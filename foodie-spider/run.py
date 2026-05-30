"""
Foodie Spider - 启动脚本
便捷的爬虫启动入口，支持命令行参数
"""

import sys
import os

# 将项目根目录加入 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_spider(spider_name="demo", **kwargs):
    """
    启动指定爬虫

    Args:
        spider_name: 爬虫名称 (demo/dianping/meituan)
        **kwargs: 传递给爬虫的参数 (city, pages 等)
    """
    settings = get_project_settings()

    # 禁用日志文件（调试时输出到终端）
    settings.set("LOG_FILE", None)
    settings.set("LOG_LEVEL", "INFO")

    process = CrawlerProcess(settings)

    spider_map = {
        "demo": "spiders.demo_data.DemoDataSpider",
        "dianping": "spiders.dianping.DianpingSpider",
    }

    if spider_name not in spider_map:
        print(f"未知爬虫: {spider_name}")
        print(f"可用爬虫: {', '.join(spider_map.keys())}")
        return

    # 动态导入爬虫类
    module_path, class_name = spider_map[spider_name].rsplit(".", 1)
    module = __import__(module_path, fromlist=[class_name])
    spider_class = getattr(module, class_name)

    print(f"\n{'='*50}")
    print(f"  启动爬虫: {spider_name}")
    print(f"  参数: {kwargs}")
    print(f"{'='*50}\n")

    process.crawl(spider_class, **kwargs)
    process.start()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Foodie Spider 爬虫启动器")
    parser.add_argument(
        "spider",
        nargs="?",
        default="demo",
        choices=["demo", "dianping"],
        help="爬虫名称 (默认: demo)",
    )
    parser.add_argument("--city", default="nanchang", help="目标城市 (默认: nanchang)")
    parser.add_argument("--pages", default=5, type=int, help="爬取页数 (默认: 5)")

    args = parser.parse_args()
    run_spider(args.spider, city=args.city, pages=args.pages)
