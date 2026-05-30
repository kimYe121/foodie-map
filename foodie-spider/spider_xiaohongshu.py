"""
Foodie Spider - 小红书爬虫（Playwright）
爬取南昌美食相关笔记，提取真实用户消费数据

数据包含:
    - 店铺名称、地址
    - 用户评分、人均消费
    - 推荐菜品
    - 点赞数、收藏数
    - 用户评论内容

运行: python spider_xiaohongshu.py --keyword "南昌美食" --pages 3
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

CATEGORY_MAP = {
    "江西菜": "jiangxi", "赣菜": "jiangxi", "拌粉": "snack",
    "火锅": "hotpot", "小吃": "snack", "快餐": "snack",
    "烧烤": "bbq", "烤肉": "bbq", "西餐": "western",
    "日料": "japan_korea", "韩餐": "japan_korea",
    "海鲜": "seafood", "甜品": "dessert", "饮品": "dessert",
    "奶茶": "dessert", "咖啡": "dessert",
    "川菜": "sichuan", "湘菜": "hunan", "粤菜": "cantonese",
}


def guess_category(text):
    for kw, code in CATEGORY_MAP.items():
        if kw in text:
            return code
    return "other"


def scrape_xiaohongshu(keyword="南昌美食", max_notes=50):
    """主爬取函数"""

    if not HAS_PLAYWRIGHT:
        print("ERROR: playwright not installed")
        return []

    all_notes = []
    seen_ids = set()

    print("=" * 55)
    print(f"  Xiaohongshu Spider - keyword: {keyword}")
    print("=" * 55)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            locale="zh-CN",
        )
        context.add_init_script('Object.defineProperty(navigator,"webdriver",{get:()=>undefined})')
        page = context.new_page()

        # 搜索页
        search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_search_result_notes"
        print(f"\n[search] {search_url}")

        try:
            page.goto(search_url, wait_until="networkidle", timeout=30000)
            time.sleep(3)

            # 滚动加载更多
            for _ in range(5):
                page.mouse.wheel(0, 1000)
                time.sleep(1)

            # 提取笔记卡片
            html = page.content()
            note_cards = extract_search_cards(html)

            print(f"  found {len(note_cards)} note cards")

            # 逐个打开笔记详情
            for i, card in enumerate(note_cards[:max_notes]):
                if card.get("note_id") in seen_ids:
                    continue
                seen_ids.add(card.get("note_id", ""))

                note_url = f"https://www.xiaohongshu.com/explore/{card['note_id']}"
                print(f"  [{i+1}/{min(len(note_cards), max_notes)}] {card.get('title', '?')[:25]}", end="")

                try:
                    page.goto(note_url, wait_until="networkidle", timeout=20000)
                    time.sleep(1)
                    detail_html = page.content()
                    note = extract_note_detail(detail_html, card)
                    if note and note.get("title"):
                        all_notes.append(note)
                        print(f" OK | like:{note.get('likes',0)} price:{note.get('price_avg',0)}")
                    else:
                        print(" empty")
                except Exception as e:
                    print(f" ERR")

                time.sleep(random.uniform(1, 2))

        except Exception as e:
            print(f"  search error: {e}")

        page.close()
        context.close()
        browser.close()

    # 保存
    print(f"\n{'='*55}")
    print(f"  Total: {len(all_notes)} notes")

    # 提取店铺信息
    shops = notes_to_shops(all_notes)
    print(f"  Extracted: {len(shops)} unique shops")

    save_json(all_notes, shops)
    save_mysql(shops)

    print("=" * 55)
    return all_notes


def extract_search_cards(html):
    """从搜索页提取笔记卡片"""
    cards = []

    # 笔记链接
    note_links = re.findall(r'href="/explore/([a-f0-9]{24})"', html)
    note_links = list(dict.fromkeys(note_links))

    # 标题
    titles = re.findall(r'"display_title":"([^"]+)"', html)

    for i, nid in enumerate(note_links):
        card = {"note_id": nid}
        if i < len(titles):
            card["title"] = titles[i]
        cards.append(card)

    return cards


def extract_note_detail(html, card):
    """从笔记详情页提取数据"""
    note = {
        "note_id": card.get("note_id", ""),
        "source": "xiaohongshu",
        "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # 标题
    title_match = re.search(r'"title":"([^"]{2,100})"', html)
    if title_match:
        note["title"] = title_match.group(1)
    elif card.get("title"):
        note["title"] = card["title"]

    # 正文内容
    desc_match = re.search(r'"desc":"([^"]{5,1000})"', html)
    if desc_match:
        note["content"] = desc_match.group(1).replace("\\n", "\n")

    # 点赞数
    likes_match = re.search(r'"liked_count":"?(\d+)"?', html)
    if likes_match:
        note["likes"] = int(likes_match.group(1))

    # 收藏数
    collect_match = re.search(r'"collected_count":"?(\d+)"?', html)
    if collect_match:
        note["collects"] = int(collect_match.group(1))

    # 评论数
    comment_match = re.search(r'"comment_count":"?(\d+)"?', html)
    if comment_match:
        note["comments"] = int(comment_match.group(1))

    # 用户名
    user_match = re.search(r'"nickname":"([^"]+)"', html)
    if user_match:
        note["author"] = user_match.group(1)

    # 从内容中提取价格信息
    text = note.get("content", "") + note.get("title", "")
    price_match = re.search(r"(\d+)\s*元/?人?|人均\s*(\d+)|¥\s*(\d+)", text)
    if price_match:
        price = price_match.group(1) or price_match.group(2) or price_match.group(3)
        note["price_avg"] = int(price)

    # 提取店铺名（常见模式：@店铺名 或 「店铺名」）
    shop_match = re.search(r"@(\S{2,20})|「([^」]+)」|《([^》]+)》", text)
    if shop_match:
        note["shop_name"] = shop_match.group(1) or shop_match.group(2) or shop_match.group(3)

    # 提取推荐菜
    dish_matches = re.findall(r"推荐[：:]?\s*(.{2,30})", text)
    if dish_matches:
        note["dishes"] = dish_matches[:3]

    # 评分（从文本提取）
    rating_match = re.search(r"(\d\.\d)\s*分|评分\s*(\d\.\d)", text)
    if rating_match:
        note["rating"] = float(rating_match.group(1) or rating_match.group(2))

    return note


def notes_to_shops(notes):
    """从笔记数据中提取店铺信息"""
    shops = {}
    for note in notes:
        name = note.get("shop_name", "")
        if not name:
            continue
        if name not in shops:
            shops[name] = {
                "shop_id": f"xhs_{hash(name) % 100000:05d}",
                "name": name,
                "source": "xiaohongshu",
                "city": "nanchang",
                "category": guess_category(note.get("title", "") + note.get("content", "")),
                "rating": note.get("rating", 0),
                "price_avg": note.get("price_avg", 0),
                "tags": note.get("dishes", []),
                "view_count": 0,
                "like_count": note.get("likes", 0),
                "comment_count": note.get("comments", 0),
                "images": [],
            }
        else:
            # 更新评分（取最高）
            if note.get("rating", 0) > shops[name].get("rating", 0):
                shops[name]["rating"] = note["rating"]
            # 更新价格（取平均）
            if note.get("price_avg", 0) > 0:
                old = shops[name].get("price_avg", 0)
                if old == 0:
                    shops[name]["price_avg"] = note["price_avg"]

    return list(shops.values())


def save_json(notes, shops, note_file="data/xhs_notes.json", shop_file="data/xhs_shops.json"):
    os.makedirs("data", exist_ok=True)
    with open(note_file, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
    print(f"[OK] {len(notes)} notes -> {note_file}")
    with open(shop_file, "w", encoding="utf-8") as f:
        json.dump(shops, f, ensure_ascii=False, indent=2)
    print(f"[OK] {len(shops)} shops -> {shop_file}")


def save_mysql(shops):
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
        INSERT INTO t_shop (shop_id, city, name, category, tags, source, rating, price_avg,
            like_count, comment_count)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), rating=VALUES(rating),
            price_avg=VALUES(price_avg), like_count=VALUES(like_count), update_time=NOW()
        """
        saved = 0
        for s in shops:
            try:
                cursor.execute(sql, (
                    s["shop_id"], "nanchang", s.get("name", ""),
                    s.get("category", "other"),
                    json.dumps(s.get("tags", []), ensure_ascii=False),
                    "xiaohongshu", s.get("rating", 0), s.get("price_avg", 0),
                    s.get("like_count", 0), s.get("comment_count", 0),
                ))
                saved += 1
            except Exception as e:
                print(f"  [DB] {s.get('name')}: {e}")
        cursor.close()
        conn.close()
        print(f"[OK] {saved}/{len(shops)} -> MySQL")
    except Exception as e:
        print(f"[ERR] MySQL: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", default="南昌美食")
    parser.add_argument("--max-notes", type=int, default=50)
    args = parser.parse_args()
    scrape_xiaohongshu(keyword=args.keyword, max_notes=args.max_notes)
