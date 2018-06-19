from unittest.mock import Mock

import pytest

from sia.spiders import SiaNodesSpider


class TestCaseSiaNodes:
    @pytest.fixture
    def spider(self):
        return SiaNodesSpider()

    @pytest.fixture
    def response(self, sia_node_json):
        response = Mock()
        response.body = '{"hosts": [' + sia_node_json + "]}"
        response.request.meta.get.return_value = 1

        return response

    @pytest.fixture
    def empty_response(self):
        response = Mock()
        response.body = '{"hosts":[]}'
        response.request.meta.get.return_value = 1

        return response

    @pytest.mark.low
    def test_init(self):
        spider = SiaNodesSpider()

        assert spider.start_urls == ["https://sia-node.goobox.io/hostdb/active/"]

    @pytest.mark.low
    def test_init_api_url(self):
        spider = SiaNodesSpider(api_url="https://foo.bar")

        assert spider.start_urls == ["https://foo.bar/hostdb/active/"]

    @pytest.mark.mid
    def test_start_requests(self, spider):
        result = list(spider.start_requests())
        expected_requests = ["https://sia-node.goobox.io/hostdb/active/"]

        assert [r.url for r in result] == expected_requests

    @pytest.mark.mid
    def test_parse(self, spider, response):
        items = list(spider.parse(response))

        assert len(items) == 1

    @pytest.mark.mid
    def test_parse_empty(self, spider, empty_response):
        result = list(spider.parse(empty_response))

        assert result == []
