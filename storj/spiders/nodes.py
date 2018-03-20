import json
from typing import Any, Dict
from urllib.parse import urlencode

from scrapy import Request

from storj import items
from core.spiders import Spider

__all__ = ['StorjNodesSpider']


class StorjNodesSpider(Spider):
    name = 'storj_nodes'
    base_url = 'https://api.storj.io/contacts'
    step = 5

    def start_requests(self):
        """
        Run N starting requests.
        """
        for i in range(1, self.step + 1):
            yield self._request_page(i)

    def parse(self, response):
        """
        Parse response, yield a request for next page and generate items from current response.

        :param response: Response.
        """
        nodes = json.loads(response.body)
        if nodes:
            yield self._request_page(response.request.meta['page'] + self.step)

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
        )

    def _request_page(self, page: int):
        url = self.base_url + f'?{urlencode({"page": page})}'
        request = Request(url, callback=self.parse)
        request.meta['page'] = page
        return request
