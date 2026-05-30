"""
Foodie Spider - MySQL 存储管道
将清洗后的数据写入 MySQL 数据库
"""

import json
from datetime import datetime

try:
    import pymysql
    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False
    print("[警告] pymysql 未安装，MySQL 管道不可用。请运行: pip install pymysql")


class MysqlPipeline:
    """MySQL 存储管道"""

    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        config = crawler.settings.getdict("MYSQL_CONFIG")
        return cls(config)

    def open_spider(self, spider):
        """爬虫启动时连接数据库"""
        if not HAS_PYMYSQL:
            spider.logger.error("pymysql 未安装，跳过 MySQL 存储")
            return

        try:
            self.conn = pymysql.connect(
                host=self.config["host"],
                port=self.config["port"],
                user=self.config["user"],
                password=self.config["password"],
                database=self.config["database"],
                charset=self.config.get("charset", "utf8mb4"),
                autocommit=True,
            )
            self.cursor = self.conn.cursor()
            spider.logger.info("MySQL 连接成功")
        except Exception as e:
            spider.logger.error(f"MySQL 连接失败: {e}")
            self.conn = None

    def close_spider(self, spider):
        """爬虫结束时关闭连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            spider.logger.info("MySQL 连接已关闭")

    def process_item(self, item, spider):
        """存储数据到 MySQL"""
        if not self.conn or not self.cursor:
            return item

        # 根据 item 类型选择存储方法
        if item.__class__.__name__ == "ShopItem":
            self._save_shop(item, spider)
        elif item.__class__.__name__ == "SpotItem":
            self._save_spot(item, spider)

        return item

    def _save_shop(self, item, spider):
        """存储店铺数据（INSERT OR UPDATE）"""
        sql = """
        INSERT INTO t_shop (
            shop_id, city, name, category, address, longitude, latitude,
            phone, business_hours, tags, source, rating, price_avg,
            shop_image, images, food_images, video_url,
            view_count, like_count, comment_count
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            category = VALUES(category),
            address = VALUES(address),
            longitude = VALUES(longitude),
            latitude = VALUES(latitude),
            phone = VALUES(phone),
            business_hours = VALUES(business_hours),
            tags = VALUES(tags),
            rating = VALUES(rating),
            price_avg = VALUES(price_avg),
            shop_image = VALUES(shop_image),
            images = VALUES(images),
            food_images = VALUES(food_images),
            video_url = VALUES(video_url),
            view_count = VALUES(view_count),
            like_count = VALUES(like_count),
            comment_count = VALUES(comment_count),
            update_time = NOW()
        """

        # 处理列表字段为 JSON 字符串
        tags = json.dumps(item.get("tags", []), ensure_ascii=False) if item.get("tags") else None
        images = json.dumps(item.get("images", []), ensure_ascii=False) if item.get("images") else None
        food_images = json.dumps(item.get("food_images", []), ensure_ascii=False) if item.get("food_images") else None

        values = (
            item.get("shop_id"),
            item.get("city", "nanchang"),
            item.get("name"),
            item.get("category"),
            item.get("address"),
            item.get("longitude"),
            item.get("latitude"),
            item.get("phone"),
            item.get("business_hours"),
            tags,
            item.get("source"),
            item.get("rating", 0),
            item.get("price_avg", 0),
            item.get("shop_image"),
            images,
            food_images,
            item.get("video_url"),
            item.get("view_count", 0),
            item.get("like_count", 0),
            item.get("comment_count", 0),
        )

        try:
            self.cursor.execute(sql, values)
            spider.logger.debug(f"保存店铺: {item.get('name')} ({item.get('shop_id')})")
        except Exception as e:
            spider.logger.error(f"保存店铺失败 [{item.get('shop_id')}]: {e}")

    def _save_spot(self, item, spider):
        """存储景点数据（INSERT OR UPDATE）"""
        sql = """
        INSERT INTO t_spot (spot_id, city, name, longitude, latitude, description, hot_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            longitude = VALUES(longitude),
            latitude = VALUES(latitude),
            description = VALUES(description),
            hot_score = VALUES(hot_score)
        """

        values = (
            item.get("spot_id"),
            item.get("city", "nanchang"),
            item.get("name"),
            item.get("longitude"),
            item.get("latitude"),
            item.get("description"),
            item.get("hot_score", 0),
        )

        try:
            self.cursor.execute(sql, values)
            spider.logger.debug(f"保存景点: {item.get('name')} ({item.get('spot_id')})")
        except Exception as e:
            spider.logger.error(f"保存景点失败 [{item.get('spot_id')}]: {e}")
