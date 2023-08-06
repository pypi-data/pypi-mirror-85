from kisters.water.rest_client import RESTClient

from ..network import Network


class NetworkStore:
    _resource = "rest", "networks"

    def __init__(self, client: RESTClient):
        self._client = client

    def list_networks(self):
        return self._client.get(self._resource)

    def get_network(self, network_uid):
        return Network(network_uid, self._client)
