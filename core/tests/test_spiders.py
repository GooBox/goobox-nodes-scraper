from unittest.mock import Mock, call, patch

import pytest

from core.spiders import Spider


class TestSpiderBase:
    @pytest.fixture
    def spider(self):
        spider = Spider('test')
        spider.crawler = Mock()
        return spider

    @pytest.mark.low
    def test_logger_property(self, spider: Spider):
        with patch('core.spiders.logging') as mock_logging:
            log = spider.logger

        assert mock_logging.getLogger.call_count == 1
        assert mock_logging.getLogger.call_args == call(f'spiders.{spider.name}')
