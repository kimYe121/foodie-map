"""
Foodie Spider - 大众点评爬虫（Playwright + Cookie + 字体解密）

核心思路:
    1. Playwright 启动浏览器，注入 Cookie 模拟登录态
    2. 浏览器渲染页面，等待 JS 加载完成
    3. 提取渲染后的 HTML，解析店铺数据
    4. 字体解密处理评分/价格等加密字段

运行前:
    1. 浏览器登录大众点评
    2. F12 → Network → 复制 Cookie
    3. 粘贴到下面 DIANPING_COOKIE

运行:
    python spider_dianping.py --pages 3
"""

import re
import json
import time
import random
import os
import sys
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

try:
    import pymysql
    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False

from config.settings import MYSQL_CONFIG


# ══════════════════════════════════════════════
#  Cookie（从浏览器复制）
# ══════════════════════════════════════════════
DIANPING_COOKIE = "_lxsdk_cuid=19e78260b5cc8-0273a23303d2d-4c657b58-146d15-19e78260b5cc8; _lxsdk=19e78260b5cc8-0273a23303d2d-4c657b58-146d15-19e78260b5cc8; _hc.v=2cdc91fd-6d44-c6df-4dbe-afd010c9412a.1780132220; fspop=test; WEBDFPID=9xx66x163u78582202w0vuvv7xxu426880v21737v7497958w5v320u8-1780218625883-1780132224948ICKMCIIfd79fef3d01d5e9aadc18ccd4d0c95072463; utm_source_rg=AM%253ewUnUP%25155%25WMMBBMsBiyjlLlvvwvzw.y..jMMyTvBllw.vsjij.jTWjWLlzL.ivwyl; qruuid=a48455eb-6ed4-4f6a-98ff-9542e2a4703e; dplet=8ddc2f5190dc79e874e3e4d07f65b7f2; dper=0202232384ce4f38b83b86e5e15cb557e39bfa9302868f7bbc3203d1ce4012e305a789eca95a0bd4601a9d4188cae12dc2f9411f0c3250de3a4400000000ad35000037148d39979e3ab12dc8e5cf4fd9eccc55f97475e00af332078e0eada0fd55131a45a9ebacdf18f8f9efff37640d3ef4; ll=7fd06e815b796be3df069dec7836c3df; ua=%E7%82%B9%E5%B0%8F%E8%AF%848169540707; ctu=84c3b8ea661e39c7162cc71b47cb630abc32bad38f42d63501add6e4156efe78; cityid=134; msource=default; default_ab=myinfo%3AA%3A1; logan_custom_report=; Hm_lvt_220e3bf81326a8b21addc0f9c967d48d=1780132941; Hm_lpvt_220e3bf81326a8b21addc0f9c967d48d=1780132941; HMACCOUNT=6A2A58629FC66EF3; _lxsdk_s=19e78260b5c-7f-93-22b%7C%7C162; logan_session_token=xw5m9vdjpjuqvj8kooq4"

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


def parse_cookies(cookie_str):
    """将 Cookie 字符串解析为 Playwright 格式"""
    cookies = []
    for item in cookie_str.split(";"):
        item = item.strip()
        if "=" in item:
            name, value = item.split("=", 1)
            cookies.append({
                "name": name.strip(),
                "value": value.strip(),
                "domain": ".dianping.com",
                "path": "/",
            })
    return cookies


def guess_category(text):
    for kw, code in CATEGORY_MAP.items():
        if kw in text:
            return code
    return "other"


def extract_number(text):
    if not text:
        return 0
    match = re.search(r"[\d.]+", text)
    return match.group() if match else "0"


def scrape_dianping(pages=3):
    """主爬取函数"""

    if not HAS_PLAYWRIGHT:
        print("ERROR: playwright not installed")
        return []

    if not DIANPING_COOKIE:
        print("ERROR: Cookie not set!")
        return []

    all_shops = []
    seen_ids = set()

    print("=" * 50)
    print("  Dianping Spider (Playwright + Cookie)")
    print("=" * 50)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])

        # 创建上下文并注入 Cookie
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            locale="zh-CN",
        )
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)

        # 注入 Cookie
        context.add_cookies(parse_cookies(DIANPING_COOKIE))
        page = context.new_page()

        # ── 遍历列表页 ──
        base_urls = [
            "https://www.dianping.com/nanchang/ch10",           # 美食全部
            "https://www.dianping.com/nanchang/ch10/g110",      # 江西菜
            "https://www.dianping.com/nanchang/ch10/g113",      # 小吃快餐
            "https://www.dianping.com/nanchang/ch10/g311",      # 火锅
            "https://www.dianping.com/nanchang/ch10/g116",      # 烧烤
            "https://www.dianping.com/nanchang/ch10/g111",      # 西餐
            "https://www.dianping.com/nanchang/ch10/g112",      # 日韩料理
        ]

        for base_url in base_urls:
            for p_num in range(1, pages + 1):
                url = f"{base_url}/p{p_num}" if p_num > 1 else base_url
                print(f"\n[page] {url}")

                try:
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    time.sleep(2)

                    # 检查验证码
                    if "verify" in page.url:
                        print("  [!] CAPTCHA! Please solve it manually in browser.")
                        print("  [!] Press Enter after solving...")
                        page.screenshot(path=f"data/captcha_{int(time.time())}.png")
                        # 等待用户手动处理
                        # input()

                    # 滚动加载
                    for _ in range(5):
                        page.mouse.wheel(0, 800)
                        time.sleep(0.5)

                    # 获取渲染后的 HTML
                    html = page.content()

                    # 提取店铺链接（支持新旧两种ID格式）
                    shop_links = re.findall(r'href="(https?://www\.dianping\.com/shop/[a-zA-Z0-9]+)"', html)
                    shop_links += re.findall(r'href="(/shop/[a-zA-Z0-9]+)"', html)
                    # 去重保序
                    shop_links = list(dict.fromkeys(shop_links))
                    # 过滤掉 /dish 和 /#comment 后缀
                    shop_links = [l for l in shop_links if "/dish" not in l and "#comment" not in l]

                    print(f"  found {len(shop_links)} shops")

                    for link in shop_links:
                        # 提取店铺ID（支持 kaYf2BIzxN26KDsF 和 123456 两种格式）
                        sid_match = re.search(r"/shop/([a-zA-Z0-9]+)", link)
                        if not sid_match:
                            continue
                        sid = f"dp_{sid_match.group(1)}"
                        if sid in seen_ids:
                            continue
                        seen_ids.add(sid)

                        # 从列表页 HTML 提取基础信息
                        shop = extract_from_list(html, sid, link)
                        if shop and shop.get("name"):
                            all_shops.append(shop)
                            print(f"  [OK] {shop['name']} | {shop.get('rating','-')} | {shop.get('price_avg','-')}yuan")

                except Exception as e:
                    print(f"  [ERR] {e}")

                time.sleep(random.uniform(2, 4))

        # ── 详情页补充信息 ──
        print(f"\n{'='*50}")
        print(f"  Fetching detail for top 30 shops...")
        print(f"{'='*50}")

        for i, shop in enumerate(all_shops[:30]):
            dp_id = shop["shop_id"].replace("dp_", "")
            url = f"https://www.dianping.com/shop/{dp_id}"
            try:
                page.goto(url, wait_until="networkidle", timeout=20000)
                time.sleep(1)
                detail_html = page.content()
                detail = extract_from_detail(detail_html, shop["shop_id"])
                if detail:
                    shop.update({k: v for k, v in detail.items() if v})
                print(f"  [{i+1}/30] {shop.get('name')} OK")
            except Exception as e:
                print(f"  [{i+1}/30] {shop.get('name')} ERR: {e}")
            time.sleep(random.uniform(2, 4))

        page.close()
        context.close()
        browser.close()

    # ── 保存 ──
    print(f"\n{'='*50}")
    print(f"  Total: {len(all_shops)} shops")
    cat_count = {}
    for s in all_shops:
        cat_count[s.get("category", "other")] = cat_count.get(s.get("category", "other"), 0) + 1
    print(f"  Categories: {cat_count}")

    save_json(all_shops)
    save_mysql(all_shops)

    print("=" * 50)
    return all_shops


def extract_from_list(html, shop_id, link):
    """从列表页 HTML 提取店铺基础信息"""
    shop = {
        "shop_id": shop_id,
        "source": "dianping",
        "city": "nanchang",
        "view_count": 0, "like_count": 0, "comment_count": 0,
        "tags": [], "images": [],
    }

    # 找到这个店铺所在的 HTML 块
    # 在 shop-list 中每个 li 是一个店铺
    pattern = rf'href="{re.escape(link)}"[^>]*>(.*?)</a>'
    match = re.search(pattern, html, re.S)
    if match:
        block_start = max(0, match.start() - 2000)
        block_end = min(len(html), match.end() + 2000)
        block = html[block_start:block_end]
    else:
        block = html

    # 名称
    name_match = re.search(r'title="([^"]+)"', block)
    if name_match:
        shop["name"] = name_match.group(1).strip()
    else:
        # 从链接文本提取
        link_text = re.search(r'>([^<]{2,30})</a>', block)
        if link_text:
            shop["name"] = link_text.group(1).strip()

    # 评分
    rating_match = re.search(r'(\d\.\d)\s*分', block)
    if rating_match:
        shop["rating"] = float(rating_match.group(1))
    else:
        shop["rating"] = 0.0

    # 人均
    price_match = re.search(r'(\d+)\s*元/人', block)
    if not price_match:
        price_match = re.search(r'人均\s*(\d+)', block)
    if price_match:
        shop["price_avg"] = int(price_match.group(1))
    else:
        shop["price_avg"] = 0

    # 地址
    addr_match = re.search(r'addr[^>]*>([^<]+)', block)
    if addr_match:
        shop["address"] = addr_match.group(1).strip()[:200]

    # 标签
    tags = re.findall(r'class="tag"[^>]*>([^<]+)', block)
    shop["tags"] = [t.strip() for t in tags if t.strip()][:5]

    # 图片
    img_match = re.search(r'<img[^>]*src="(https?://[^"]+)"', block)
    if img_match:
        shop["shop_image"] = img_match.group(1)

    # 分类
    shop["category"] = guess_category(
        shop.get("name", "") + " ".join(shop.get("tags", []))
    )

    return shop


def extract_from_detail(html, shop_id):
    """从详情页提取更多信息"""
    detail = {"shop_id": shop_id}

    # 名称
    name_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    if name_match:
        detail["name"] = re.sub(r'<[^>]+>', '', name_match.group(1)).strip()

    # 评分 - 多种模式匹配
    for pat in [
        r'(\d\.\d)\s*分',                     # "4.4分"
        r'score[^>]*>([\d.]+)',               # score元素
        r'item.*?review.*?(\d\.\d)',          # 评论区评分
        r'brief.*?(\d\.\d)',                  # 简介区评分
    ]:
        m = re.search(pat, html)
        if m:
            try:
                val = float(m.group(1))
                if 0 < val <= 5:
                    detail["rating"] = val
                    break
            except ValueError:
                pass
    if "rating" not in detail:
        detail["rating"] = 0.0

    # 人均消费 - 多种模式匹配
    for pat in [
        r'(\d+)\s*元/人',                     # "97元/人"
        r'人均[^\d]*(\d+)',                    # "人均 97"
        r'price.*?(\d{2,4})',                 # price元素
    ]:
        m = re.search(pat, html)
        if m:
            try:
                val = int(m.group(1))
                if 5 < val < 500:
                    detail["price_avg"] = val
                    break
            except ValueError:
                pass
    if "price_avg" not in detail:
        detail["price_avg"] = 0

    # 电话
    phone_match = re.search(r'(\d{3,4}[-\s]?\d{7,8})', html)
    if phone_match:
        detail["phone"] = phone_match.group(1)[:200]

    # 地址 - 多种模式匹配
    for pat in [
        r'地址[：:]\s*([^<]{5,200})',
        r'addr[^>]*class[^>]*>([^<]{5,200})',
        r'address[^>]*>([^<]{5,200})',
    ]:
        m = re.search(pat, html)
        if m:
            addr = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            if len(addr) > 5 and "css" not in addr:
                detail["address"] = addr[:200]
                break

    # 营业时间
    for pat in [
        r'营业时间[：:]\s*([^<]+)',
        r'business.*?hours[^>]*>([^<]+)',
    ]:
        m = re.search(pat, html)
        if m:
            detail["business_hours"] = m.group(1).strip()[:100]
            break

    return detail


def save_json(shops, filepath="data/dianping_shops.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(shops, f, ensure_ascii=False, indent=2)
    print(f"[OK] saved {len(shops)} to {filepath}")


def save_mysql(shops):
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
                    s["shop_id"], "nanchang", s.get("name", ""), s.get("category", "other"),
                    s.get("address"), s.get("longitude"), s.get("latitude"),
                    s.get("phone"), s.get("business_hours"),
                    json.dumps(s.get("tags", []), ensure_ascii=False),
                    "dianping", s.get("rating", 0), s.get("price_avg", 0),
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=3)
    args = parser.parse_args()
    scrape_dianping(pages=args.pages)
