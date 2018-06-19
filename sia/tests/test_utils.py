import pytest

from sia.utils import SiaNodeDecoder


class TestCaseSiaNodeDecoder:
    @pytest.fixture
    def decoder(self):
        return SiaNodeDecoder()

    @pytest.mark.mid
    def test_decode(self, decoder, sia_node, sia_node_json):
        result = decoder.decode('{"hosts":[' + sia_node_json + "]}")

        assert result == [sia_node]

    @pytest.mark.low
    def test_decode_list_with_empty_node(self, decoder):
        result = decoder.decode('{"hosts":[{}]}')

        assert result == [{}]
