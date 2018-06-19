import json
import typing
from urllib.parse import urljoin

import scrapy

from core.spiders import Spider
from sia import items
from sia.utils import SiaNodeDecoder

__all__ = ["SiaNodesSpider"]


class SiaNodesSpider(Spider):
    name = "sia_nodes"
    base_url = "https://sia-node.goobox.io"

    def __init__(self, *args, api_url: typing.Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        if not api_url:
            api_url = self.base_url

        self.start_urls = [urljoin(api_url, "/hostdb/active")]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True, headers={"User-Agent": "Sia-Agent"})

    def parse(self, response):
        """
        Parse response, yield a request for next page and generate items from current response.

        @url https://sia-node.goobox.io/hostdb/active/
        @returns requests 1
        @returns items 1
        @scrapes address to_resolve_geolocation
        """
        for node in json.loads(response.body, cls=SiaNodeDecoder):
            yield from self.parse_node(node)

    def parse_node(self, node: typing.Dict[str, typing.Any]):
        """
        Generate a new Item from parsed node.

        :param node: Storj node data.
        """
        address, port = node["netaddress"].split(":")

        yield items.SiaNode(
            last_historic_update=node.get("LastHistoricUpdate"),
            accepting_contracts=node.get("acceptingcontracts"),
            address=address,
            port=port,
            collateral=node.get("collateral"),
            contract_price=node.get("contractprice"),
            download_bandwidth_price=node.get("downloadbandwidthprice"),
            first_seen=node.get("firstseen"),
            historic_downtime=node.get("historicdowntime"),
            historic_failed_interactions=node.get("historicfailedinteractions"),
            historic_successful_interactions=node.get("historicsuccessfulinteractions"),
            historic_uptime=node.get("historicuptime"),
            max_collateral=node.get("maxcollateral"),
            max_download_batch_size=node.get("maxdownloadbatchsize"),
            max_duration=node.get("maxduration"),
            max_revise_batch_size=node.get("maxrevisebatchsize"),
            public_key=node.get("publickey"),
            recent_failed_interactions=node.get("recentfailedinteractions"),
            recent_successful_interactions=node.get("recentsuccessfulinteractions"),
            remaining_storage=node.get("remainingstorage"),
            revision_number=node.get("revisionnumber"),
            scan_history=node.get("scanhistory"),
            sector_size=node.get("sectorsize"),
            storage_price=node.get("storageprice"),
            total_storage=node.get("totalstorage"),
            unlock_hash=node.get("unlockhash"),
            upload_bandwidth_price=node.get("uploadbandwidthprice"),
            version=node.get("version"),
            window_size=node.get("windowsize"),
            to_resolve_geolocation=address,
        )
