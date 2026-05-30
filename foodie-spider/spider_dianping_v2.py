"""
Foodie Spider - 大众点评爬虫 v2（基于 CSDN 教程优化）

核心思路:
    1. requests 直接请求（不依赖 Playwright）
    2. PC 网站搜索店铺列表 + 详情页
    3. 移动端 API 获取评论数据（JSON 格式，无需字体解密）
    4. Cookie 模拟登录态

运行:
    python spider_dianping_v2.py --city 南昌 --pages 5
"""

import requests
import time
import string
import random
import json
import csv
import os
import re
import sys
import argparse
from lxml import html as lxml_html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import pymysql
    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False

from config.settings import MYSQL_CONFIG


# ══════════════════════════════════════════════
#  Cookie（从浏览器复制）
# ══════════════════════════════════════════════
DIANPING_COOKIE = "_lxsdk_cuid=19e78260b5cc8-0273a23303d2d-4c657b58-146d15-19e78260b5cc8; _lxsdk=19e78260b5cc8-0273a23303d2d-4c657b58-146d15-19e78260b5cc8; _hc.v=2cdc91fd-6d44-c6df-4dbe-afd010c9412a.1780132220; fspop=test; WEBDFPID=9xx66x163u78582202w0vuvv7xxu426880v21737v7497958w5v320u8-1780218625883-1780132224948ICKMCIIfd79fef3d01d5e9aadc18ccd4d0c95072463; dplet=8ddc2f5190dc79e874e3e4d07f65b7f2; dper=0202232384ce4f38b83b86e5e15cb557e39bfa9302868f7bbc3203d1ce4012e305a789eca95a0bd4601a9d4188cae12dc2f9411f0c3250de3a4400000000ad35000037148d39979e3ab12dc8e5cf4fd9eccc55f97475e00af332078e0eada0fd55131a45a9ebacdf18f8f9efff37640d3ef4; ll=7fd06e815b796be3df069dec7836c3df; ua=%E7%82%B9%E5%B0%8F%E8%AF%848169540707; ctu=84c3b8ea661e39c7162cc71b47cb630abc32bad38f42d63501add6e4156efe78; cityid=134; logan_session_token=xw5m9vdjpjuqvj8kooq4"

# 城市ID映射
CITY_IDS = {
    "南昌": 347, "武汉": 56, "长沙": 34, "北京": 2, "上海": 1,
    "广州": 7, "深圳": 340, "成都": 59, "杭州": 3, "南京": 10,
}

# ── 请求头 ──
PC_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
    "cookie": DIANPING_COOKIE,
    "referer": "https://www.dianping.com/",
}

M_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
    "cookie": DIANPING_COOKIE,
    "host": "mapi.dianping.com",
    "origin": "https://m.dianping.com",
    "referer": "https://m.dianping.com/",
}

# 分类映射
CATEGORY_MAP = {
    "江西菜": "jiangxi", "赣菜": "jiangxi",
    "火锅": "hotpot",
    "小吃": "snack", "快餐": "snack", "粉面": "snack", "拌粉": "snack",
    "烧烤": "bbq", "烤肉": "bbq",
    "西餐": "western",
    "日料": "japan_korea", "韩餐": "japan_korea",
    "海鲜": "seafood",
    "甜品": "dessert", "饮品": "dessert", "奶茶": "dessert",
    "川菜": "sichuan", "湘菜": "hunan", "粤菜": "cantonese",
}


def gen_query_id():
    """生成 mapi 需要的 queryid"""
    ts = str(int(time.time() * 1000))
    rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=13))
    return f"{ts}_{rand}"


def guess_category(text):
    for kw, code in CATEGORY_MAP.items():
        if kw in text:
            return code
    return "other"


# ══════════════════════════════════════════════
#  1. 搜索店铺
# ══════════════════════════════════════════════
def search_shops(city_id, keyword, pages=3):
    """搜索店铺列表"""
    all_shops = []

    for page in range(1, pages + 1):
        url = f"https://www.dianping.com/search/keyword/{city_id}/0_{keyword}/p{page}"
        print(f"  [search] page {page}: {url}")

        try:
            resp = requests.get(url, headers=PC_HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"    status: {resp.status_code}, skip")
                continue

            tree = lxml_html.fromstring(resp.text)
            li_list = tree.xpath('//div[contains(@class,"shop-list")]/ul/li')

            for li in li_list:
                try:
                    name = li.xpath('.//h4/text()')
                    name = name[0].strip() if name else None
                    link = li.xpath('.//h4/../@href')
                    link = link[0] if link else None

                    if not name or not link:
                        continue

                    sid_match = re.search(r"shop/([a-zA-Z0-9]+)", link)
                    if not sid_match:
                        continue
                    shop_id = sid_match.group(1)

                    # 评分
                    rating = 0.0
                    star_el = li.xpath('.//span[contains(@class,"score")]/text()')
                    if star_el:
                        m = re.search(r"(\d\.\d)", star_el[0])
                        if m:
                            rating = float(m.group(1))

                    # 人均
                    price = 0
                    price_el = li.xpath('.//a[contains(@class,"mean-price")]/text()')
                    if price_el:
                        m = re.search(r"(\d+)", price_el[0])
                        if m:
                            price = int(m.group(1))

                    # 标签
                    tags = li.xpath('.//span[@class="tag"]/text()')
                    tags = [t.strip() for t in tags if t.strip()][:5]

                    all_shops.append({
                        "shop_id": f"dp_{shop_id}",
                        "name": name,
                        "rating": rating,
                        "price_avg": price,
                        "tags": tags,
                        "url": f"https://www.dianping.com{link}" if not link.startswith("http") else link,
                    })
                except Exception:
                    continue

            print(f"    found {len(li_list)} shops on this page")
        except Exception as e:
            print(f"    error: {e}")

        time.sleep(random.uniform(1, 2))

    return all_shops


# ══════════════════════════════════════════════
#  2. 店铺详情
# ══════════════════════════════════════════════
def get_shop_detail(shop):
    """获取店铺详情页信息"""
    url = shop.get("url", "")
    if not url:
        return shop

    try:
        resp = requests.get(url, headers=PC_HEADERS, timeout=15)
        if resp.status_code != 200:
            return shop

        tree = lxml_html.fromstring(resp.text)

        # 地址
        addr = tree.xpath('//span[@class="addressText wx-text"]/text()')
        if addr:
            shop["address"] = addr[0].strip()

        # 电话
        phone_match = re.findall(r'"phoneNos":\s*\["?(\d+)"?\]', resp.text)
        if phone_match:
            shop["phone"] = phone_match[0]

        # 营业时间
        hours = tree.xpath('//div[contains(@class,"left-service")]//text()')
        hours = " ".join(h.strip() for h in hours if h.strip())
        if hours:
            shop["business_hours"] = hours[:100]

        # 评论数
        review_el = tree.xpath('//span[@class="reviews wx-text"]/text()')
        if review_el:
            m = re.search(r"(\d+)", review_el[0])
            if m:
                shop["comment_count"] = int(m.group(1))

        # 图片
        img = tree.xpath('//div[contains(@class,"shop-photo")]//img/@src')
        if img:
            shop["shop_image"] = img[0] if img[0].startswith("http") else "https:" + img[0]

    except Exception:
        pass

    return shop


# ══════════════════════════════════════════════
#  3. 评论数据（移动端 API）
# ══════════════════════════════════════════════
def fetch_comments(shop_id, start=0):
    """抓取一页评论"""
    dp_id = shop_id.replace("dp_", "")
    query_id = gen_query_id()

    url = (
        "https://mapi.dianping.com/mapi/review/outsidesiftedreviewlist.bin?"
        f"optimus_code=10&optimus_partner=76&optimus_risk_level=71&"
        f"reqsource=4&filterid=800&merge=1&needfilter=1&"
        f"queryid={query_id}&referid={dp_id}&refertype=0&"
        f"start={start}&multifilterids=%7B%22filterIds%22%3A%5B800%5D%7D&"
        f"yodaReady=h5&csecplatform=4&csecversion=4.1.1"
    )

    try:
        resp = requests.get(url, headers=M_HEADERS, timeout=10)
        data = resp.json()

        if not isinstance(data, dict):
            return True, []

        review_list = data.get("list", [])
        if not isinstance(review_list, list):
            return True, []

        is_end = data.get("isEnd", True)
        comments = []

        for item in review_list:
            if not isinstance(item, dict):
                continue
            feed_user = item.get("feedUser", {})
            if not isinstance(feed_user, dict):
                continue
            username = feed_user.get("userName", "")
            if not username or username == "商家回应":
                continue

            content = item.get("content", "")
            score_list = item.get("feedScoreList") or []
            score_text = " ".join(
                s.get("text", "") for s in score_list if isinstance(s, dict)
            )

            comments.append({
                "username": username,
                "content": content.replace("\n", "")[:500],
                "score_text": score_text,
                "shop_id": shop_id,
            })

        return is_end, comments
    except Exception:
        return True, []


def crawl_all_comments(shop_id, max_pages=10):
    """爬取一个店铺的所有评论"""
    all_comments = []
    start = 0

    for _ in range(max_pages):
        is_end, comments = fetch_comments(shop_id, start)
        if comments:
            all_comments.extend(comments)
        if is_end:
            break
        start += 14
        time.sleep(random.uniform(0.5, 1.5))

    return all_comments


# ══════════════════════════════════════════════
#  4. 存储
# ══════════════════════════════════════════════
def save_shops_json(shops, filepath="data/dianping_v2_shops.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(shops, f, ensure_ascii=False, indent=2)
    print(f"[OK] {len(shops)} shops -> {filepath}")


def save_comments_csv(comments, filepath="data/dianping_v2_comments.csv"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "content", "score_text", "shop_id"])
        writer.writeheader()
        writer.writerows(comments)
    print(f"[OK] {len(comments)} comments -> {filepath}")


def save_shops_mysql(shops):
    if not HAS_PYMYSQL:
        return
    try:
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"], port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"], password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"], charset="utf8mb4", autocommit=True,
        )
        cursor = conn.cursor()
        sql = """
        INSERT INTO t_shop (shop_id, city, name, category, address, phone, business_hours,
            tags, source, rating, price_avg, shop_image, comment_count)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), rating=VALUES(rating),
            price_avg=VALUES(price_avg), comment_count=VALUES(comment_count), update_time=NOW()
        """
        saved = 0
        for s in shops:
            try:
                cursor.execute(sql, (
                    s["shop_id"], "nanchang", s.get("name", ""),
                    guess_category(s.get("name", "") + " ".join(s.get("tags", []))),
                    s.get("address"), s.get("phone"), s.get("business_hours"),
                    json.dumps(s.get("tags", []), ensure_ascii=False),
                    "dianping", s.get("rating", 0), s.get("price_avg", 0),
                    s.get("shop_image"), s.get("comment_count", 0),
                ))
                saved += 1
            except Exception as e:
                print(f"  [DB] {s.get('name')}: {e}")
        cursor.close()
        conn.close()
        print(f"[OK] {saved}/{len(shops)} -> MySQL")
    except Exception as e:
        print(f"[ERR] MySQL: {e}")


# ══════════════════════════════════════════════
#  5. 主流程
# ══════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="Dianping Spider v2")
    parser.add_argument("--city", default="南昌", help="城市名")
    parser.add_argument("--pages", type=int, default=3, help="搜索页数")
    parser.add_argument("--comments", action="store_true", help="是否爬取评论")
    parser.add_argument("--max-comments", type=int, default=5, help="每家店铺最大评论页数")
    args = parser.parse_args()

    city_id = CITY_IDS.get(args.city, 347)
    print("=" * 55)
    print(f"  Dianping Spider v2 - {args.city} (city_id={city_id})")
    print("=" * 55)

    # 搜索关键词
    keywords = ["美食", "江西菜", "火锅", "小吃", "烧烤", "甜品"]

    all_shops = []
    seen_ids = set()

    for kw in keywords:
        print(f"\n--- keyword: {kw} ---")
        shops = search_shops(city_id, kw, pages=args.pages)
        for s in shops:
            if s["shop_id"] not in seen_ids:
                seen_ids.add(s["shop_id"])
                all_shops.append(s)
        print(f"  cumulative: {len(all_shops)} unique shops")

    # 详情页补全
    print(f"\n{'='*55}")
    print(f"  Fetching detail for {len(all_shops)} shops...")
    print(f"{'='*55}")

    for i, shop in enumerate(all_shops):
        shop = get_shop_detail(shop)
        all_shops[i] = shop
        r = shop.get("rating", 0)
        p = shop.get("price_avg", 0)
        n = shop.get("name", "?")[:14]
        print(f"  [{i+1}/{len(all_shops)}] {n} | r={r} p={p}")
        time.sleep(random.uniform(0.5, 1))

    # 评论数据
    all_comments = []
    if args.comments:
        print(f"\n{'='*55}")
        print(f"  Fetching comments...")
        print(f"{'='*55}")

        for i, shop in enumerate(all_shops[:50]):
            sid = shop["shop_id"]
            comments = crawl_all_comments(sid, max_pages=args.max_comments)
            all_comments.extend(comments)
            print(f"  [{i+1}] {shop.get('name','?')[:14]} -> {len(comments)} comments")
            time.sleep(random.uniform(0.5, 1))

    # 保存
    print(f"\n{'='*55}")
    print(f"  Total: {len(all_shops)} shops, {len(all_comments)} comments")
    cat_count = {}
    for s in all_shops:
        cat = guess_category(s.get("name", "") + " ".join(s.get("tags", [])))
        cat_count[cat] = cat_count.get(cat, 0) + 1
    print(f"  Categories: {cat_count}")

    save_shops_json(all_shops)
    save_shops_mysql(all_shops)
    if all_comments:
        save_comments_csv(all_comments)

    print("=" * 55)


if __name__ == "__main__":
    main()
