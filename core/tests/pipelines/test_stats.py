import datetime
from unittest.mock import MagicMock, Mock, call, patch

import pytest
import scrapy

from core.items import Item
from core.pipelines.stats import StatsPipeline


class TestStatsPipeline:
    @pytest.fixture
    def pipeline(self):
        return StatsPipeline(stats=MagicMock())

    @pytest.fixture
    def item(self):
        class FooItem(Item):
            id = scrapy.Field()
            foo = scrapy.Field(required=True)
            bar = scrapy.Field()

        return FooItem()

    @pytest.fixture
    def spider(self):
        spider = Mock(spec=scrapy.Spider)
        spider.name = 'foo_spider'
        return spider

    @pytest.mark.mid
    def test_from_crawler(self, pipeline):
        expected_call = [call('foo')]

        with patch.object(StatsPipeline, '__init__', return_value=None) as pipeline_mock:
            crawler_mock = Mock()
            crawler_mock.stats = 'foo'
            pipeline.from_crawler(crawler_mock)

        assert pipeline_mock.call_args_list == expected_call

    @pytest.mark.high
    @pytest.mark.freeze_time
    def test_open_spider(self, pipeline, spider):
        expected_calls = [call('spider/foo_spider/start', datetime.datetime.utcnow())]

        pipeline.open_spider(spider)

        assert pipeline.stats.set_value.call_args_list == expected_calls

    @pytest.mark.high
    @pytest.mark.freeze_time
    def test_close_spider(self, pipeline, spider):
        expected_calls = [call('spider/foo_spider/finish', datetime.datetime.utcnow())]
        expected_items = {'crawled_items', 'dropped_items', 'start_time', 'finish_time', 'item_foo'}

        pipeline.stats.get_stats.return_value = {'item/foo': 2, 'item/foo/dropped': 1}

        pipeline.close_spider(spider)

        assert pipeline.stats.set_value.call_args_list == expected_calls

        extra_fields = spider.logger.info.call_args[1]['extra']
        assert set(extra_fields.keys()) == expected_items

    @pytest.mark.high
    def test_process_item(self, item, pipeline, spider):
        expected_calls = [call('item/fooitem'), call('spider/foo_spider/foo')]

        processed_item = pipeline.process_item(item, spider)

        assert processed_item == item
        assert pipeline.stats.inc_value.call_args_list == expected_calls
