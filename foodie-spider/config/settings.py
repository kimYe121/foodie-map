"""
Foodie Spider - Scrapy 配置文件
"""

# ── 基本配置 ──
BOT_NAME = "foodie-spider"
SPIDER_MODULES = ["spiders"]
NEWSPIDER_MODULE = "spiders"

# ── 请求配置 ──
ROBOTSTXT_OBEY = False  # 目标网站 robots.txt 可能限制爬虫
CONCURRENT_REQUESTS = 4  # 并发请求数，降低以避免被封
DOWNLOAD_DELAY = 2  # 请求间隔（秒），模拟人类行为
CONCURRENT_REQUESTS_PER_DOMAIN = 2  # 单域名并发数
RANDOMIZE_DOWNLOAD_DELAY = True  # 随机化延迟 (0.5x ~ 1.5x)

# ── UA 伪装 ──
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
]

# ── Headers ──
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

# ── 中间件 ──
DOWNLOADER_MIDDLEWARES = {
    "middlewares.random_ua.RandomUserAgentMiddleware": 400,
    "middlewares.random_ua.RandomProxyMiddleware": 410,
}

# ── 数据管道 ──
ITEM_PIPELINES = {
    "pipelines.data_clean.CleanPipeline": 100,       # 数据清洗
    "pipelines.data_dedupe.DedupePipeline": 200,     # 去重
}

# pymysql 已安装时启用 MySQL 管道
try:
    import pymysql
    ITEM_PIPELINES["pipelines.data_mysql.MysqlPipeline"] = 300
except ImportError:
    pass

# ── MySQL 配置 ──
MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456!",  # 请填写你的 MySQL 密码
    "database": "foodie_map",
    "charset": "utf8mb4",
}

# ── 阿里云 OSS 配置 ──
OSS_CONFIG = {
    "access_key_id": "",       # 请填写
    "access_key_secret": "",   # 请填写
    "endpoint": "oss-cn-nanchang.aliyuncs.com",
    "bucket_name": "foodie-map-img",
    "domain": "https://foodie-map-img.oss-cn-nanchang.aliyuncs.com",
}

# ── 爬虫目标配置 ──
TARGET_CITIES = {
    "nanchang": {"name": "南昌", "province": "江西"},
    # "wuhan": {"name": "武汉", "province": "湖北"},      # 后续扩展
    # "changsha": {"name": "长沙", "province": "湖南"},    # 后续扩展
}

# ── 日志配置 ──
LOG_LEVEL = "INFO"
LOG_FILE = "data/spider.log"
LOG_FILEMODE = "a"

# ── 缓存配置（调试时可开启，避免重复请求） ──
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # 缓存 24 小时
HTTPCACHE_DIR = "data/httpcache"

# ── 其他 ──
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
CLOSESPIDER_ITEMCOUNT = 0  # 0 表示不限制
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
