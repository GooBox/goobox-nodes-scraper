import scrapy

__all__ = ["Item"]


class RequiredFieldsMixin:
    @classmethod
    def get_required_fields(cls):
        if not hasattr(cls, "_required"):
            cls._required = [k for k, v in cls.fields.items() if v.get("required")]

        return cls._required


class Item(RequiredFieldsMixin, scrapy.Item):
    pass
