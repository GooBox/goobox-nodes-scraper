BOT_NAME = "GooboxNodes"

SPIDER_MODULES = [
    "storj.spiders",
    "sia.spiders",
]

DEFAULT_ITEM_CLASS = "core.items.Item"

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

DOWNLOAD_DELAY = 0.2

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
}

LOG_LEVEL = "INFO"

FAKEUSERAGENT_FALLBACK = "Mozilla"

ITEM_PIPELINES = {
    "core.pipelines.resolve_geolocation.ResolveGeolocationPipeline": 100,
    "core.pipelines.required_fields.RequiredFieldsPipeline": 200,
    "core.pipelines.stats.StatsPipeline": 900,
}
