"""
Foodie Spider - 高德地图 POI 爬虫
通过高德开放平台 API 爬取南昌美食餐厅数据

优势:
    - 合法合规（高德开放平台官方 API）
    - 数据结构化（名称/地址/坐标/评分/电话一应俱全）
    - 稳定可靠（不会被封 IP）

使用前:
    1. 去 https://lbs.amap.com 注册账号
    2. 创建应用，获取 Web服务 API Key
    3. 把 Key 填入下面的 AMAP_KEY 变量

运行: python spider_amap.py
"""

import json
import time
import os
import sys
import math
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests

try:
    import pymysql
    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False

from config.settings import MYSQL_CONFIG

# ══════════════════════════════════════════════
#  在这里填写你的高德 API Key
#  申请地址: https://lbs.amap.com/dev/key/app
# ══════════════════════════════════════════════
AMAP_KEY = "f944287466cea9b73714bbe488952046"  # <-- 填写你的 Key


# 高德 API 地址
AMAP_POI_URL = "https://restapi.amap.com/v3/place/text"
AMAP_GEO_URL = "https://restapi.amap.com/v3/geocode/geo"

# 南昌市中心坐标
NANCHANG_CENTER = "115.8928,28.6820"

# 美食分类代码 (高德 POI 分类)
FOOD_TYPES = "050000"  # 050000 = 餐饮服务

# 细分分类
FOOD_SUBTYPES = {
    "050100": "中餐厅",
    "050200": "外国餐厅",
    "050300": "小吃快餐",
    "050400": "咖啡厅",
    "050500": "茶馆",
    "050600": "甜品店",
}

# 分类映射到我们的 category
TYPE_TO_CATEGORY = {
    "中餐厅": "jiangxi",
    "江西菜": "jiangxi", "赣菜": "jiangxi",
    "火锅店": "hotpot", "火锅": "hotpot",
    "小吃": "snack", "快餐": "snack", "粉面馆": "snack",
    "烧烤": "bbq", "烤肉": "bbq",
    "西餐厅": "western",
    "日本料理": "japan_korea", "韩国料理": "japan_korea",
    "海鲜": "seafood",
    "甜品": "dessert", "饮品": "dessert", "咖啡厅": "dessert", "奶茶": "dessert",
    "川菜": "sichuan", "湘菜": "hunan", "粤菜": "cantonese",
}


def guess_category(name, type_name):
    """根据店铺名和分类名猜测分类"""
    for kw, code in TYPE_TO_CATEGORY.items():
        if kw in name or kw in type_name:
            return code
    # 按大类映射
    if "中餐" in type_name:
        return "jiangxi"
    if "快餐" in type_name or "小吃" in type_name:
        return "snack"
    if "咖啡" in type_name or "甜品" in type_name or "饮品" in type_name:
        return "dessert"
    if "外国" in type_name:
        return "western"
    return "other"


def haversine(lon1, lat1, lon2, lat2):
    """计算两点距离(km)"""
    R = 6371
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return round(R * 2 * math.asin(math.sqrt(a)), 2)


def fetch_pois(key, keywords="", types=FOOD_TYPES, city="南昌", page=1, page_size=25):
    """调用高德 POI 搜索接口 (Web服务 API，只需 Key)"""
    params = {
        "key": key,
        "keywords": keywords,
        "types": types,
        "city": city,
        "citylimit": "true",
        "offset": page_size,
        "page": page,
        "extensions": "all",
        "output": "json",
    }

    resp = requests.get(AMAP_POI_URL, params=params, timeout=10)
    data = resp.json()

    if data.get("status") != "1":
        print(f"  [API ERROR] {data.get('info', 'unknown error')}")
        return [], 0

    pois = data.get("pois", [])
    total = int(data.get("count", 0))
    return pois, total


def parse_poi(poi):
    """将高德 POI 数据转换为我们的格式"""
    # 坐标
    location = poi.get("location", "0,0").split(",")
    lng = float(location[0]) if len(location) > 0 else 0
    lat = float(location[1]) if len(location) > 1 else 0

    # 评分
    rating = 0.0
    biz_ext = poi.get("biz_ext", {})
    if biz_ext:
        rating_str = biz_ext.get("rating", "")
        if rating_str:
            try:
                rating = float(rating_str)
            except ValueError:
                rating = 0.0

    # 人均消费
    cost = 0
    if biz_ext:
        cost_str = biz_ext.get("cost", "")
        if cost_str:
            try:
                cost = int(float(cost_str))
            except ValueError:
                cost = 0

    # 分类
    type_name = poi.get("type", "")
    name = poi.get("name", "")
    category = guess_category(name, type_name)

    # 图片
    photos = poi.get("photos", [])
    shop_image = photos[0].get("url", "") if photos else ""
    images = [p.get("url", "") for p in photos[:10]]

    return {
        "shop_id": f"amap_{poi.get('id', '')}",
        "name": name,
        "category": category,
        "address": poi.get("address", ""),
        "longitude": lng,
        "latitude": lat,
        "phone": str(poi.get("tel", ""))[:200],
        "business_hours": poi.get("business_hours", ""),
        "rating": rating,
        "price_avg": cost,
        "tags": [t.strip() for t in (poi.get("tag", "").split(";") if isinstance(poi.get("tag", ""), str) else poi.get("tag", [])) if t.strip()],
        "shop_image": shop_image,
        "images": images,
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "source": "amap",
    }


def save_to_json(shops, filepath="data/amap_shops.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(shops, f, ensure_ascii=False, indent=2)
    print(f"[OK] saved {len(shops)} to {filepath}")


def save_to_mysql(shops):
    if not HAS_PYMYSQL:
        print("[WARN] pymysql not installed")
        return
    try:
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"], port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"], password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"], charset="utf8mb4", autocommit=True,
        )
        cursor = conn.cursor()
        sql = """
        INSERT INTO t_shop (shop_id, city, name, category, address, longitude, latitude,
            phone, business_hours, tags, source, rating, price_avg, shop_image, images,
            view_count, like_count, comment_count)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), rating=VALUES(rating),
            price_avg=VALUES(price_avg), tags=VALUES(tags), update_time=NOW()
        """
        saved = 0
        for s in shops:
            try:
                cursor.execute(sql, (
                    s["shop_id"], "nanchang", s["name"], s["category"],
                    s.get("address"), s.get("longitude"), s.get("latitude"),
                    s.get("phone"), s.get("business_hours"),
                    json.dumps(s.get("tags", []), ensure_ascii=False),
                    "amap", s.get("rating", 0), s.get("price_avg", 0),
                    s.get("shop_image"),
                    json.dumps(s.get("images", []), ensure_ascii=False),
                    0, 0, 0,
                ))
                saved += 1
            except Exception as e:
                print(f"  [DB] {s.get('name')}: {e}")
        cursor.close()
        conn.close()
        print(f"[OK] saved {saved}/{len(shops)} to MySQL")
    except Exception as e:
        print(f"[ERROR] MySQL: {e}")


def scrape_amap(max_pages=10):
    """主爬取函数"""
    if not AMAP_KEY:
        print("=" * 55)
        print("  ERROR: 请先填写高德 API Key!")
        print()
        print("  步骤:")
        print("  1. 打开 https://lbs.amap.com/dev/key/app")
        print("  2. 注册/登录，创建应用")
        print("  3. 添加 Key，选择 Web服务 类型")
        print("  4. 复制 Key，粘贴到 spider_amap.py 的 AMAP_KEY 变量")
        print("=" * 55)
        return []

    all_shops = []
    seen_ids = set()

    print("=" * 55)
    print("  Foodie Spider - Amap POI (Nanchang Food)")
    print("=" * 55)

    # 搜索多种关键词以覆盖更多店铺
    search_keywords = [
        "",              # 全部美食
        "江西菜",        # 本地特色
        "火锅",          # 火锅
        "小吃",          # 小吃快餐
        "烧烤",          # 烧烤
        "甜品饮品",      # 甜品
    ]

    for keyword in search_keywords:
        label = keyword if keyword else "全部美食"
        print(f"\n--- searching: {label} ---")

        for page in range(1, max_pages + 1):
            pois, total = fetch_pois(AMAP_KEY, keywords=keyword, page=page)

            if not pois:
                break

            print(f"  page {page}: {len(pois)} results (total: {total})")

            for poi in pois:
                shop = parse_poi(poi)
                sid = shop["shop_id"]

                if sid in seen_ids:
                    continue
                seen_ids.add(sid)

                # 去掉不在南昌市区的 (坐标范围过滤)
                if not (115.7 < shop["longitude"] < 116.1 and 28.5 < shop["latitude"] < 29.0):
                    continue

                all_shops.append(shop)

            # 高德 API 限制: 每秒 100 次，免费用户每天 5000 次
            time.sleep(0.5)

            if page * 25 >= total:
                break

    print(f"\n{'=' * 55}")
    print(f"  done: {len(all_shops)} unique shops")

    if all_shops:
        cat_count = {}
        for s in all_shops:
            cat_count[s.get("category", "other")] = cat_count.get(s.get("category", "other"), 0) + 1
        print(f"  categories: {cat_count}")

        save_to_json(all_shops)
        save_to_mysql(all_shops)

    print("=" * 55)
    return all_shops


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=10, help="max pages per keyword")
    args = parser.parse_args()
    scrape_amap(max_pages=args.pages)
