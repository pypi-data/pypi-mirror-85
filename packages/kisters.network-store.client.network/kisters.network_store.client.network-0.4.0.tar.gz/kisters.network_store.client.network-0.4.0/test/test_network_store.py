import os

import pytest

from kisters.network_store.client.network_store import NetworkStore
from kisters.water.rest_client import RESTClient
from kisters.water.rest_client.auth import OpenIDConnect

rest_client = RESTClient(
    url=os.environ["NETWORK_STORE_URL"],
    authentication=OpenIDConnect(
        client_id=os.environ["CLIENT_ID"], client_secret=os.environ["CLIENT_SECRET"]
    ),
)

try:
    rest_client.get("rest/networks")
except Exception:
    pytestmark = pytest.mark.skip(
        "Currently no publicly available network store service"
    )


def test_store():
    store = NetworkStore(rest_client)
    store.list_networks()
    network = store.get_network("tmp")
    network.drop()
