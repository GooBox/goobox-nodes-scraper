import logging

import scrapy

__all__ = ["Spider"]


class Spider(scrapy.Spider):
    @property
    def logger(self):
        return logging.getLogger(f"spiders.{self.name}")
