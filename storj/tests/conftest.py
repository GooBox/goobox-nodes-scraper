import datetime
import pytest


@pytest.fixture
def storj_node_json():
    return '{"spaceAvailable":true,"lastSeen":"2018-03-26T14:45:00.000Z","port":9165,"address":"62.251.79.52",' \
           '"protocol":"1.2.0","responseTime":11322.960065021764,"userAgent":"8.7.2","reputation":2785,' \
           '"lastTimeout":"2018-03-26T14:45:00.000Z","nodeID":"0cb4d8b9d945928b7cb18015a06c9fe9bb35f4fd"}'


@pytest.fixture
def storj_node():
    return {
        'address': '62.251.79.52',
        'lastSeen': datetime.datetime(2018, 3, 26, 14, 45, 0, 0),
        'lastTimeout': datetime.datetime(2018, 3, 26, 14, 45, 0, 0),
        'nodeID': '0cb4d8b9d945928b7cb18015a06c9fe9bb35f4fd',
        'port': 9165,
        'protocol': '1.2.0',
        'reputation': 2785,
        'responseTime': 11322.960065021764,
        'spaceAvailable': True,
        'userAgent': '8.7.2'
    }
