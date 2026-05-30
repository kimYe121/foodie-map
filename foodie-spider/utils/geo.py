"""
Foodie Spider - 地理计算工具
计算两点间距离（球面距离公式）
"""

import math


def haversine(lon1, lat1, lon2, lat2):
    """
    计算两个经纬度坐标之间的距离（公里）
    使用 Haversine 公式

    Args:
        lon1, lat1: 第一个点的经度、纬度
        lon2, lat2: 第二个点的经度、纬度

    Returns:
        距离（公里），保留两位小数
    """
    R = 6371  # 地球半径（公里）

    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return round(R * c, 2)


def is_within_radius(lon1, lat1, lon2, lat2, radius_km):
    """
    判断两点是否在指定半径内

    Args:
        lon1, lat1: 中心点坐标
        lon2, lat2: 目标点坐标
        radius_km: 半径（公里）

    Returns:
        bool
    """
    return haversine(lon1, lat1, lon2, lat2) <= radius_km


# ── 南昌主要景点坐标 ──
NANCHANG_SPOTS = {
    "tengwangge": {
        "name": "滕王阁",
        "longitude": 115.8890,
        "latitude": 28.6842,
        "description": "江南三大名楼之一，南昌地标",
        "hot_score": 100,
    },
    "bayi": {
        "name": "八一广场",
        "longitude": 115.9123,
        "latitude": 28.6820,
        "description": "南昌市中心广场，八一南昌起义纪念地",
        "hot_score": 95,
    },
    "shengjin": {
        "name": "绳金塔",
        "longitude": 115.8980,
        "latitude": 28.6740,
        "description": "南昌地标性建筑，千年古塔",
        "hot_score": 85,
    },
    "qiushui": {
        "name": "秋水广场",
        "longitude": 115.8760,
        "latitude": 28.6900,
        "description": "亚洲最大音乐喷泉群",
        "hot_score": 90,
    },
    "bayibu": {
        "name": "八一起义纪念馆",
        "longitude": 115.9100,
        "latitude": 28.6800,
        "description": "国家一级博物馆",
        "hot_score": 88,
    },
    "meiling": {
        "name": "梅岭国家森林公园",
        "longitude": 115.7500,
        "latitude": 28.8500,
        "description": "南昌后花园，避暑胜地",
        "hot_score": 80,
    },
}
