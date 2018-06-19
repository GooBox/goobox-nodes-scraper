import datetime
from unittest.mock import Mock

import pytest

from storj.spiders import StorjNodesSpider


class TestStorjNodes:
    @pytest.fixture
    def spider(self):
        return StorjNodesSpider(last_seen="1900-1-1T00:00:00.000Z")

    @pytest.fixture
    def response(self, storj_node_json):
        response = Mock()
        response.body = "[" + storj_node_json + "]"
        response.request.meta.get.return_value = 1

        return response

    @pytest.fixture
    def empty_response(self):
        response = Mock()
        response.body = "[]"
        response.request.meta.get.return_value = 1

        return response

    @pytest.mark.low
    def test_init(self):
        last_seen_filter = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        last_seen_filter = last_seen_filter.replace(hour=0, minute=0, second=0, microsecond=0)

        spider = StorjNodesSpider()

        assert spider._step == 5
        assert spider._last_seen_filter == last_seen_filter

    @pytest.mark.low
    def test_init_last_seen(self):
        last_seen_filter = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        last_seen_filter = last_seen_filter.replace(hour=0, minute=0, second=0, microsecond=0)
        last_seen = last_seen_filter.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        spider = StorjNodesSpider(last_seen=last_seen)

        assert spider._step == 5
        assert spider._last_seen_filter == last_seen_filter

    @pytest.mark.mid
    def test_start_requests(self, spider):
        result = list(spider.start_requests())
        expected_requests = [spider.base_url + f"?page={i}" for i in range(1, spider._step + 1)]

        assert [r.url for r in result] == expected_requests

    @pytest.mark.mid
    def test_parse(self, spider, response):
        result = list(spider.parse(response))
        next_request, items = result[0], result[1:]

        assert next_request.url == spider.base_url + f"?page={spider._step + 1}"
        assert len(items) == 1

    @pytest.mark.mid
    def test_parse_empty(self, spider, empty_response):
        result = list(spider.parse(empty_response))

        assert result == []
