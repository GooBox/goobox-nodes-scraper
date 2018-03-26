import socket
from unittest.mock import Mock, call, patch

import geoip2.database
import pytest
import scrapy
from geoip2.errors import AddressNotFoundError
from scrapy.exceptions import DropItem

from core.exceptions import InitializationError
from core.items import Item
from core.pipelines.resolve_geolocation import ResolveGeolocationPipeline
from core.tests.utils import create_tarfile_mock


class TestResolveGeolocationPipeline:
    @pytest.fixture
    def pipeline(self):
        with patch.object(ResolveGeolocationPipeline, '__init__', return_value=None):
            yield ResolveGeolocationPipeline()

    @pytest.fixture
    def item(self):
        class FooItem(Item):
            to_resolve_geolocation = scrapy.Field()
            country = scrapy.Field()
            city = scrapy.Field()
            latitude = scrapy.Field()
            longitude = scrapy.Field()

        return FooItem()

    @pytest.fixture
    def spider(self):
        spider = Mock(spec=scrapy.Spider)
        spider.name = 'foo_spider'
        return spider

    @pytest.mark.mid
    def test_init_download_file_with_invalid_content(self):
        tarfile_mock = create_tarfile_mock('foo.bar')
        tarfile_mock.__enter__.return_value = tarfile_mock

        with patch('core.pipelines.resolve_geolocation.urllib.request.urlretrieve'), \
                patch('core.pipelines.resolve_geolocation.tarfile.open', return_value=tarfile_mock), \
                pytest.raises(InitializationError):
            ResolveGeolocationPipeline()

    @pytest.mark.mid
    def test_from_crawler(self, pipeline):
        expected_call = [call()]

        with patch.object(ResolveGeolocationPipeline, '__init__', return_value=None) as pipeline_mock:
            crawler_mock = Mock()
            pipeline.from_crawler(crawler_mock)

        assert pipeline_mock.call_args_list == expected_call

    @pytest.mark.high
    def test_process_item(self, item, spider):
        pipeline = ResolveGeolocationPipeline()

        assert isinstance(pipeline.resolver, geoip2.database.Reader)

        item['to_resolve_geolocation'] = 'www.google.com'

        processed_item = pipeline.process_item(item, spider)

        assert processed_item['country'] == 'United States'
        assert processed_item['city'] == 'Mountain View'
        assert processed_item['latitude'] == 37.419200000000004
        assert processed_item['longitude'] == -122.0574

    @pytest.mark.mid
    def test_process_item_drop_name_not_resolve(self, item, pipeline, spider):
        item['to_resolve_geolocation'] = 'foobar'

        with patch('core.pipelines.resolve_geolocation.socket.gethostbyname', side_effect=socket.gaierror), \
                pytest.raises(DropItem):
            pipeline.process_item(item, spider)

    @pytest.mark.mid
    def test_process_item_drop_address_not_found(self, item, pipeline, spider):
        item['to_resolve_geolocation'] = 'foobar'

        resolver_mock = Mock()
        resolver_mock.city.side_effect = AddressNotFoundError
        pipeline.resolver = resolver_mock
        with patch('core.pipelines.resolve_geolocation.socket.gethostbyname'), pytest.raises(DropItem):
            pipeline.process_item(item, spider)

    @pytest.mark.mid
    def test_process_item_without_geolocation(self, item, pipeline, spider):
        processed_item = pipeline.process_item(item, spider)

        assert 'to_resolve_geolocation' not in processed_item
        assert 'country' not in processed_item
        assert 'city' not in processed_item
        assert 'latitude' not in processed_item
        assert 'longitude' not in processed_item
