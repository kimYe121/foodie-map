"""
Foodie Spider - 去重管道
基于 shop_id 去重，同一店铺多平台取并集
"""


class DedupePipeline:
    """去重管道：基于 shop_id 去重"""

    def __init__(self):
        self.seen_ids = set()

    def process_item(self, item, spider):
        shop_id = item.get("shop_id")
        if not shop_id:
            spider.logger.warning(f"缺少 shop_id，丢弃: {item.get('name')}")
            return None

        if shop_id in self.seen_ids:
            spider.logger.debug(f"重复数据，跳过: {shop_id} ({item.get('name')})")
            return None

        self.seen_ids.add(shop_id)
        return item
