from unittest.mock import Mock, call, patch

import pytest
import scrapy
from scrapy.exceptions import DropItem

from core.items import BaseItem
from core.pipelines.required_fields import RequiredFieldsPipeline


class TestRequiredFieldsPipeline:
    @pytest.fixture
    def pipeline(self):
        return RequiredFieldsPipeline(stats=Mock())

    @pytest.fixture
    def item(self):
        class FooItem(BaseItem):
            id = scrapy.Field()
            foo = scrapy.Field(required=True)
            bar = scrapy.Field()

        return FooItem()

    @pytest.fixture
    def spider(self):
        spider = Mock(spec=scrapy.Spider)
        spider.name = 'foo_spider'
        return spider

    @pytest.mark.core
    @pytest.mark.high
    def test_from_crawler(self, pipeline):
        expected_call = [call('foo')]

        with patch.object(RequiredFieldsPipeline, '__init__', return_value=None) as pipeline_mock:
            crawler_mock = Mock()
            crawler_mock.stats = 'foo'
            pipeline.from_crawler(crawler_mock)

        assert pipeline_mock.call_args_list == expected_call

    @pytest.mark.core
    @pytest.mark.high
    def test_process_item(self, item, pipeline, spider):
        item['foo'] = 'bar'

        processed_item = pipeline.process_item(item, spider)

        assert processed_item == item

    @pytest.mark.core
    @pytest.mark.high
    def test_process_item_drop(self, item, pipeline, spider):
        with pytest.raises(DropItem):
            pipeline.process_item(item, spider)

    @pytest.mark.core
    @pytest.mark.high
    def test_process_item_drop_with_id(self, item, pipeline, spider):
        item['id'] = 'id'

        with pytest.raises(DropItem):
            pipeline.process_item(item, spider)

    @pytest.mark.core
    @pytest.mark.high
    def test_process_unknown_item(self, pipeline, spider):
        item = scrapy.Item()

        processed_item = pipeline.process_item(item, spider)

        assert processed_item == item
