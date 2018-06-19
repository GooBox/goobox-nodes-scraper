import pytest

from storj.utils import StorjNodeDecoder


class TestCaseStorjNodeDecoder:
    @pytest.fixture
    def decoder(self):
        return StorjNodeDecoder()

    @pytest.mark.mid
    def test_decode(self, decoder, storj_node, storj_node_json):
        result = decoder.decode("[" + storj_node_json + "]")

        assert result == [storj_node]

    @pytest.mark.low
    def test_decode_list_with_empty_node(self, decoder):
        result = decoder.decode("[{}]")

        assert result == [{}]
