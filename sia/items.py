import scrapy

from core.items import Item


class SiaNode(Item):
    last_historic_update = scrapy.Field()  # LastHistoricUpdate
    accepting_contracts = scrapy.Field()  # acceptingcontracts
    address = scrapy.Field()  # netaddress
    collateral = scrapy.Field()  # collateral
    contract_price = scrapy.Field()  # contractprice
    download_bandwidth_price = scrapy.Field()  # downloadbandwidthprice
    first_seen = scrapy.Field()  # firstseen
    historic_downtime = scrapy.Field()  # historicdowntime
    historic_failed_interactions = scrapy.Field()  # historicfailedinteractions
    historic_successful_interactions = scrapy.Field()  # historicsuccessfulinteractions
    historic_uptime = scrapy.Field()  # historicuptime
    max_collateral = scrapy.Field()  # maxcollateral
    max_download_batch_size = scrapy.Field()  # maxdownloadbatchsize
    max_duration = scrapy.Field()  # maxduration
    max_revise_batch_size = scrapy.Field()  # maxrevisebatchsize
    port = scrapy.Field()  # netaddress
    public_key = scrapy.Field()  # publickey
    recent_failed_interactions = scrapy.Field()  # recentfailedinteractions
    recent_successful_interactions = scrapy.Field()  # recentsuccessfulinteractions
    remaining_storage = scrapy.Field()  # remainingstorage
    revision_number = scrapy.Field()  # revisionnumber
    scan_history = scrapy.Field()  # scanhistory
    sector_size = scrapy.Field()  # sectorsize
    storage_price = scrapy.Field()  # storageprice
    total_storage = scrapy.Field()  # totalstorage
    unlock_hash = scrapy.Field()  # unlockhash
    upload_bandwidth_price = scrapy.Field()  # uploadbandwidthprice
    version = scrapy.Field()  # version
    window_size = scrapy.Field()  # windowsize

    # Required fields for ResolveGeolocationPipeline
    to_resolve_geolocation = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
