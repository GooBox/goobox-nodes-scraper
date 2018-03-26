from scrapy.exceptions import DropItem

from core.items import Item


class RequiredFieldsPipeline:
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def process_item(self, item, spider):
        if isinstance(item, Item):
            difference = set(item.get_required_fields()) - set(item.keys())
            if difference:
                self.stats.inc_value(f'item/{item.__class__.__name__.lower()}/dropped')
                self.stats.inc_value(f'spider/{spider.name}/dropped')

                msg = f'Missing field{"s" if len(difference) > 1 else ""}: {", ".join(difference)}.'
                if item.get('id'):
                    msg += f' Item "{item["id"]}".'
                raise DropItem(msg)

        return item
