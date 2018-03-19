import re

import datetime

__all__ = ['StatsPipeline']

ITEM_REGEX = re.compile(r'^item/([a-zA-Z_]+)$')


class StatsPipeline:
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def open_spider(self, spider):
        self.stats.set_value(f'spider/{spider.name}/start', datetime.datetime.utcnow())

    def close_spider(self, spider):
        self.stats.set_value(f'spider/{spider.name}/finish', datetime.datetime.utcnow())

        extra = {
            'crawled_items': self.stats.get_value(f'spider/{spider.name}/foo', 0),
            'dropped_items': self.stats.get_value(f'spider/{spider.name}/dropped', 0),
            'start_time': self.stats.get_value(f'spider/{spider.name}/start').isoformat(),
            'finish_time': self.stats.get_value(f'spider/{spider.name}/finish').isoformat(),
        }

        # Add foo count
        for k, v in self.stats.get_stats().items():
            match = ITEM_REGEX.match(k)
            if match:
                extra[f'item_{match.group(1)}'] = v

        spider.logger.info('Spider %s finished successfully', spider.name, extra=extra)

    def process_item(self, item, spider):
        self.stats.inc_value(f'item/{item.__class__.__name__.lower()}')
        self.stats.inc_value(f'spider/{spider.name}/foo')

        return item
