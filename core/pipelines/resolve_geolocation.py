import os
import socket
import tarfile
import tempfile
import urllib.request

import geoip2.database
from geoip2.errors import AddressNotFoundError
from scrapy.exceptions import DropItem


class ResolveGeolocation:
    def __init__(self, stats):
        with tempfile.TemporaryDirectory() as tmp:
            downloaded_file = os.path.join(tmp, 'geolite.tar.gz')
            urllib.request.urlretrieve('http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz',
                                       filename=downloaded_file)
            with tarfile.open(downloaded_file, 'r:gz') as tar:
                db_file_name = next((i for i in tar.getnames() if i.endswith('.mmdb')))
                tar.extract(tar.getmember(db_file_name), tmp)

            self.resolver = geoip2.database.Reader(os.path.join(tmp, db_file_name))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def process_item(self, item, spider):
        if item['to_resolve_geolocation']:
            try:
                host = socket.gethostbyname(item['to_resolve_geolocation'])
                resolution = self.resolver.city(host)
                item['country'] = resolution.country.name
                item['city'] = resolution.city.name
                item['latitude'] = resolution.location.latitude
                item['longitude'] = resolution.location.longitude
                del item['to_resolve_geolocation']
            except (AddressNotFoundError, socket.gaierror):
                raise DropItem(f'Location not found for address {item["to_resolve_geolocation"]}')

        return item
