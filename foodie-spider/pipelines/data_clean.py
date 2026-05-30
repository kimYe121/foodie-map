"""
Foodie Spider - 数据清洗管道
过滤无用信息、格式标准化、字段校验
"""

import re
from datetime import datetime


class CleanPipeline:
    """数据清洗管道：过滤、标准化、校验"""

    def process_item(self, item, spider):
        """清洗单条数据"""

        # 1. 必填字段校验
        if not item.get("name"):
            spider.logger.warning(f"缺少店铺名称，丢弃: {item}")
            return None

        # 2. 店铺名称清洗
        item["name"] = self._clean_text(item.get("name", ""))

        # 3. 地址清洗
        if item.get("address"):
            item["address"] = self._clean_text(item["address"])

        # 4. 评分标准化 (转为 float, 范围 0-5)
        if item.get("rating") is not None:
            item["rating"] = self._normalize_rating(item["rating"])
        else:
            item["rating"] = 0.0

        # 5. 价格标准化 (转为 int, 单位: 元)
        if item.get("price_avg") is not None:
            item["price_avg"] = self._normalize_price(item["price_avg"])
        else:
            item["price_avg"] = 0

        # 6. 标签清洗 (转为列表)
        if item.get("tags"):
            item["tags"] = self._clean_tags(item["tags"])
        else:
            item["tags"] = []

        # 7. 坐标校验
        if item.get("longitude") and item.get("latitude"):
            item["longitude"] = self._normalize_coord(item["longitude"], -180, 180)
            item["latitude"] = self._normalize_coord(item["latitude"], -90, 90)

        # 8. 浏览数/点赞数/评论数 默认 0
        for field in ["view_count", "like_count", "comment_count"]:
            if not item.get(field):
                item[field] = 0

        # 9. 填充元数据
        item["crawl_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return item

    @staticmethod
    def _clean_text(text):
        """清洗文本：去除首尾空白、多余空格、特殊字符"""
        if not text:
            return ""
        text = str(text).strip()
        text = re.sub(r"\s+", " ", text)  # 多个空白合并
        text = re.sub(r"[\x00-\x1f]", "", text)  # 去除控制字符
        return text

    @staticmethod
    def _normalize_rating(value):
        """评分标准化为 0-5 的 float"""
        try:
            rating = float(value)
            if rating > 5:
                rating = rating / 2  # 有些平台是 10 分制
            return round(max(0, min(5, rating)), 1)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def _normalize_price(value):
        """价格标准化为 int (元)"""
        try:
            if isinstance(value, str):
                # 去除 "¥", "元", "," 等字符
                value = re.sub(r"[¥￥元,，]", "", value).strip()
                # 处理 "50/人" 这种格式
                match = re.search(r"(\d+)", value)
                if match:
                    value = match.group(1)
            price = int(float(value))
            return max(0, price)
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def _clean_tags(tags):
        """标签清洗：转为列表，去空去重"""
        if isinstance(tags, str):
            # 逗号分隔的字符串
            tags = [t.strip() for t in re.split(r"[,，、|]", tags) if t.strip()]
        elif isinstance(tags, (list, tuple)):
            tags = [str(t).strip() for t in tags if t]
        else:
            return []
        # 去重保序
        seen = set()
        result = []
        for t in tags:
            if t not in seen:
                seen.add(t)
                result.append(t)
        return result

    @staticmethod
    def _normalize_coord(value, min_val, max_val):
        """坐标标准化"""
        try:
            coord = float(value)
            return round(max(min_val, min(max_val, coord)), 7)
        except (ValueError, TypeError):
            return None
