"""
Foodie Spider - 数据模型定义
定义爬虫采集的数据结构，对应 MySQL 中的表字段
"""

import scrapy


class ShopItem(scrapy.Item):
    """店铺数据项，对应 t_shop 表"""

    # 基本信息
    shop_id = scrapy.Field()          # 店铺唯一标识 (如 dp_123456)
    name = scrapy.Field()             # 店铺名称
    city = scrapy.Field()             # 所属城市 (nanchang/wuhan/changsha)
    category = scrapy.Field()         # 美食分类
    address = scrapy.Field()          # 地址
    longitude = scrapy.Field()        # 经度
    latitude = scrapy.Field()         # 纬度
    phone = scrapy.Field()            # 电话
    business_hours = scrapy.Field()   # 营业时间
    tags = scrapy.Field()             # 标签列表 ['tag1', 'tag2']
    source = scrapy.Field()           # 数据来源 (dianping/meituan/xiaohongshu/douyin)

    # 评分与消费
    rating = scrapy.Field()           # 综合评分 (0-5)
    price_avg = scrapy.Field()        # 人均消费 (元)

    # 图片 (存 OSS URL)
    shop_image = scrapy.Field()       # 店铺封面图
    images = scrapy.Field()           # 店铺图片列表
    food_images = scrapy.Field()      # 美食图片列表
    video_url = scrapy.Field()        # 视频 URL

    # 互动数据
    view_count = scrapy.Field()       # 浏览数
    like_count = scrapy.Field()       # 点赞数
    comment_count = scrapy.Field()    # 评论数

    # 元数据
    crawl_url = scrapy.Field()        # 爬取来源 URL
    crawl_time = scrapy.Field()       # 爬取时间


class SpotItem(scrapy.Item):
    """景点数据项，对应 t_spot 表"""

    spot_id = scrapy.Field()          # 景点唯一标识
    name = scrapy.Field()             # 景点名称
    city = scrapy.Field()             # 所属城市
    longitude = scrapy.Field()        # 经度
    latitude = scrapy.Field()         # 纬度
    description = scrapy.Field()      # 景点描述
    hot_score = scrapy.Field()        # 热度评分


class ShopSpotItem(scrapy.Item):
    """店铺-景点关联数据项，对应 t_shop_spot 表"""

    shop_id = scrapy.Field()          # 店铺 ID
    spot_id = scrapy.Field()          # 景点 ID
    distance = scrapy.Field()         # 距离 (公里)
