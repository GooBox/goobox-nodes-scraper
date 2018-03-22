import json
from typing import Any, Dict
from urllib.parse import urlencode

import datetime
from scrapy import Request

from storj import items
from core.spiders import Spider

__all__ = ['StorjNodesSpider']


class StorjNodeDecoder(json.JSONDecoder):
    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def decode(self, *args, **kwargs):
        nodes = super().decode(*args, **kwargs)

        for node in nodes:

            if 'lastSeen' in node:
                node['lastSeen'] = datetime.datetime.strptime(node['lastSeen'], self.datetime_format)

            if 'lastTimeout' in node:
                node['lastTimeout'] = datetime.datetime.strptime(node['lastTimeout'], self.datetime_format)

        return nodes


class StorjNodesSpider(Spider):
    name = 'storj_nodes'
    base_url = 'https://api.storj.io/contacts'

    def __init__(self, last_seen=None, step=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._step = step
        if last_seen is None:
            self._last_seen_filter = datetime.datetime.utcnow() - datetime.timedelta(days=1)
            self._last_seen_filter = self._last_seen_filter.replace(hour=0, minute=0, second=0)
        else:
            self._last_seen_filter = datetime.datetime.strptime(last_seen, '%Y-%m-%dT%H:%M:%S.%fZ')

    def start_requests(self):
        """
        Run N starting requests.
        """
        for i in range(1, self._step + 1):
            yield self._request_page(i)

    def parse(self, response):
        """
        Parse response, yield a request for next page and generate items from current response.

        :param response: Response.
        """
        nodes = [i for i in json.loads(response.body, cls=StorjNodeDecoder)
                 if 'lastSeen' in i and i['lastSeen'] > self._last_seen_filter]
        if nodes:
            yield self._request_page(response.request.meta['page'] + self._step)

            for node in nodes:
                yield from self.parse_node(node)

    def parse_node(self, node: Dict[str, Any]):
        """
        Generate a new Item from parsed node.

        :param node: Storj node data.
        """
        yield items.StorjNode(
            space_available=node.get('spaceAvailable'),
            last_seen=node.get('lastSeen'),
            port=node['port'],
            address=node['address'],
            protocol=node['protocol'],
            response_time=node.get('responseTime'),
            user_agent=node.get('userAgent'),
            reputation=node.get('reputation'),
            last_timeout=node.get('lastTimeout'),
            timeout_rate=node.get('timeoutRate'),
            node_id=node['nodeID'],
            to_resolve_geolocation=node['address'],
        )

    def _request_page(self, page: int):
        url = self.base_url + f'?{urlencode({"page": page})}'
        request = Request(url, callback=self.parse)
        request.meta['page'] = page
        return request
