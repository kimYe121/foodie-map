"""
批量补全大众点评店铺的评分、价格、地址等详情数据
3个浏览器页并发，速度约 0.5s/家
"""

import json, re, time, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright
from spider_dianping import (
    DIANPING_COOKIE, parse_cookies, extract_from_detail, save_json, save_mysql
)


def main():
    with open("data/dianping_shops.json", "r", encoding="utf-8") as f:
        shops = json.load(f)

    # 只补全评分或价格为0的
    need_fix = [s for s in shops if s.get("rating", 0) == 0 or s.get("price_avg", 0) == 0]
    print(f"total: {len(shops)}, need fix: {len(need_fix)}")

    # 代理配置（开梯子后填本地代理端口）
    PROXY = os.environ.get("HTTP_PROXY", "")  # 例: http://127.0.0.1:7890

    with sync_playwright() as p:
        launch_args = {"headless": True, "args": ["--no-sandbox"]}
        if PROXY:
            launch_args["proxy"] = {"server": PROXY}
            print(f"using proxy: {PROXY}")
        browser = p.chromium.launch(**launch_args)
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
            locale="zh-CN",
        )
        ctx.add_init_script('Object.defineProperty(navigator,"webdriver",{get:()=>undefined})')
        ctx.add_cookies(parse_cookies(DIANPING_COOKIE))

        pages = [ctx.new_page() for _ in range(3)]
        start = time.time()
        success = 0

        for i, shop in enumerate(need_fix):
            dp_id = shop["shop_id"].replace("dp_", "")
            url = f"https://www.dianping.com/shop/{dp_id}"
            pg = pages[i % 3]
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=12000)
                time.sleep(0.3)
                html = pg.content()
                detail = extract_from_detail(html, shop["shop_id"])
                if detail:
                    shop.update({k: v for k, v in detail.items() if v})
                    success += 1
                r = shop.get("rating", 0)
                c = shop.get("price_avg", 0)
                n = shop.get("name", "?")[:14]
                print(f"[{i+1}/{len(need_fix)}] {n} | r={r} p={c}")
            except Exception:
                print(f"[{i+1}/{len(need_fix)}] ERR")
            time.sleep(0.2)

        elapsed = time.time() - start
        print(f"\n{success}/{len(need_fix)} fixed in {elapsed:.1f}s")

        for pg in pages:
            pg.close()
        ctx.close()
        browser.close()

    save_json(shops)
    save_mysql(shops)
    print("DONE")


if __name__ == "__main__":
    main()
