import pytest
import scrapy

from core.items import RequiredFieldsMixin


class TestRequiredFieldsMixin:
    @pytest.fixture
    def item(self):
        class Foo(RequiredFieldsMixin, scrapy.Item):
            foo = scrapy.Field(required=True)
            bar = scrapy.Field()

        return Foo

    @pytest.mark.high
    def test_get_required_fields(self, item):
        expected_fields = ["foo"]

        fields = item.get_required_fields()

        assert expected_fields == fields

    @pytest.mark.low
    def test_get_schema_twice(self, item):
        expected_fields = ["foo"]

        fields = item.get_required_fields()
        assert expected_fields == fields

        fields2 = item.get_required_fields()
        assert expected_fields == fields2
