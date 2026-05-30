"""
Foodie Spider - 随机 UA & 代理中间件
反爬措施：轮换 User-Agent、IP 代理
"""

import random
from scrapy import signals


class RandomUserAgentMiddleware:
    """随机 User-Agent 中间件"""

    def __init__(self, ua_list):
        self.ua_list = ua_list

    @classmethod
    def from_crawler(cls, crawler):
        ua_list = crawler.settings.getlist("USER_AGENT_LIST", [])
        if not ua_list:
            ua_list = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36"
            ]
        return cls(ua_list)

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(self.ua_list)


class RandomProxyMiddleware:
    """
    随机代理中间件
    TODO: 接入代理 IP 池，当前为空实现
    """

    PROXY_LIST = [
        # "http://ip1:port",
        # "http://ip2:port",
    ]

    def process_request(self, request, spider):
        if self.PROXY_LIST:
            proxy = random.choice(self.PROXY_LIST)
            request.meta["proxy"] = proxy
            spider.logger.debug(f"Using proxy: {proxy}")
