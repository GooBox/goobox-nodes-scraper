import scrapy

from core.items import Item


class StorjNode(Item):
    space_available = scrapy.Field()
    last_seen = scrapy.Field()
    port = scrapy.Field()
    address = scrapy.Field()
    protocol = scrapy.Field()
    response_time = scrapy.Field()
    user_agent = scrapy.Field()
    reputation = scrapy.Field()
    last_timeout = scrapy.Field()
    timeout_rate = scrapy.Field()
    node_id = scrapy.Field()
