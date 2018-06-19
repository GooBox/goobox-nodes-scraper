import datetime

import pytest


@pytest.fixture
def sia_node_json():
    return """{"acceptingcontracts":true,"maxdownloadbatchsize":9999999999,"maxduration":20160,
    "maxrevisebatchsize":9999999999,"netaddress":"1.1.1.1:9982","remainingstorage":6992005431296,
    "sectorsize":4194304,"totalstorage":7000796692480,
    "unlockhash":"1ac5acb930a7c4b125436effb234862fa97236e63748bf9587555d06e98c8130cda0dec4a547","windowsize":144,
    "collateral":"104166666666","maxcollateral":"1000000000000000000000000000",
    "contractprice":"300000000000000000000000","downloadbandwidthprice":"1000000000000","storageprice":"462962962",
    "uploadbandwidthprice":"5000000000000","revisionnumber":1595408,"version":"1.3.3","firstseen":151248,
    "historicdowntime":0,"historicuptime":2321164170507582,
    "scanhistory":[{"timestamp":"2018-06-19T08:01:05.150867468Z","success":true}],"historicfailedinteractions":0,
    "historicsuccessfulinteractions":0,"recentfailedinteractions":0,"recentsuccessfulinteractions":155,
    "LastHistoricUpdate":0,"publickey":{"algorithm":"ed25519","key":"d1Kj6tFnCxgmSUo4LtmOvQUTiyIUTd20LHijzbfNATw="},
    "publickeystring":"ed25519:7752a3ead1670b1826494a382ed98ebd05138b22144dddb42c78a3cdb7cd013c"}"""


@pytest.fixture
def sia_node():
    return {
        "acceptingcontracts": True,
        "maxdownloadbatchsize": 9999999999,
        "maxduration": 20160,
        "maxrevisebatchsize": 9999999999,
        "netaddress": "1.1.1.1:9982",
        "remainingstorage": 6992005431296,
        "sectorsize": 4194304,
        "totalstorage": 7000796692480,
        "unlockhash": "1ac5acb930a7c4b125436effb234862fa97236e63748bf9587555d06e98c8130cda0dec4a547",
        "windowsize": 144,
        "collateral": "104166666666",
        "maxcollateral": "1000000000000000000000000000",
        "contractprice": "300000000000000000000000",
        "downloadbandwidthprice": "1000000000000",
        "storageprice": "462962962",
        "uploadbandwidthprice": "5000000000000",
        "revisionnumber": 1595408,
        "version": "1.3.3",
        "firstseen": 151248,
        "historicdowntime": 0,
        "historicuptime": 2321164170507582,
        "scanhistory": [{"timestamp": datetime.datetime(2018, 6, 19, 8, 1, 5, 150867), "success": True}],
        "historicfailedinteractions": 0,
        "historicsuccessfulinteractions": 0,
        "recentfailedinteractions": 0,
        "recentsuccessfulinteractions": 155,
        "LastHistoricUpdate": 0,
        "publickey": {"algorithm": "ed25519", "key": "d1Kj6tFnCxgmSUo4LtmOvQUTiyIUTd20LHijzbfNATw="},
        "publickeystring": "ed25519:7752a3ead1670b1826494a382ed98ebd05138b22144dddb42c78a3cdb7cd013c",
    }
