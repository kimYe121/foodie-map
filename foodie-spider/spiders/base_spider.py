"""
Foodie Spider - 基础爬虫类
封装通用的爬取逻辑，子类只需实现 parse_item 方法
"""

import scrapy
from abc import abstractmethod
from datetime import datetime
from items import ShopItem


class BaseSpider(scrapy.Spider):
    """
    基础爬虫抽象类

    面向对象设计：
    - 封装性：通用逻辑封装在基类
    - 继承性：子类继承基类，复用代码
    - 多态性：子类重写 parse_item 实现不同平台的解析逻辑
    - 抽象类：parse_item 定义为抽象方法，强制子类实现
    """

    def __init__(self, city="nanchang", pages=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city = city
        self.pages = int(pages)
        self.platform = self._get_platform_name()
        self.logger.info(f"初始化爬虫: 平台={self.platform}, 城市={city}, 页数={pages}")

    @abstractmethod
    def _get_platform_name(self):
        """返回平台标识，子类必须实现"""
        pass

    @abstractmethod
    def start_requests(self):
        """生成起始请求，子类必须实现"""
        pass

    @abstractmethod
    def parse_item(self, response):
        """解析页面数据，子类必须实现，返回 ShopItem"""
        pass

    def create_shop_item(self):
        """创建带有默认值的 ShopItem"""
        item = ShopItem()
        item["city"] = self.city
        item["source"] = self.platform
        item["view_count"] = 0
        item["like_count"] = 0
        item["comment_count"] = 0
        return item

    def log_result(self, item):
        """记录采集结果"""
        self.logger.info(
            f"[{self.platform}] {item.get('name')} | "
            f"评分:{item.get('rating')} | "
            f"人均:{item.get('price_avg')}元 | "
            f"分类:{item.get('category')}"
        )
