# Hydraulic Network Client Library

This library allows connections to remote hydraulic network REST servers. It
supports authentication with OpenID Connect.

## Installation

Install with `pip`:

```bash
> python -m pip install kisters.network_store.client.network
# or you if also need the water models
> python -m pip install kisters.network_store.client.network[water]
```


## Example Usage

### Create the Kisters REST Client

```python
from kisters.water.rest_client import RESTClient
from kisters.water.rest_client.auth import OpenIDConnect


rest_client = RESTClient(
    url="https://jesse-test.hydraulic-network.kisters.cloud",
    authentication=OpenIDConnect(
        client_id="jesse-test",
        client_secret="c4b0f70d-d2e6-497f-b11c-d49fe806c29b",
    ),
)

# Verify the client is set up correctly
# Note: If you have not created any networks yet, this could be an empty list
rest_client.get(("rest", "networks"))
# ['my-network', 'my-other-network', ...]
```

### Connect to a Network

```python
from kisters.water.hydraulic_network.client import Network

# Instantiate the Network class with the network name and client
network = Network("my-network", rest_client)

# You can now access the properties of the network
network.get_nodes()
# [
# FlowBoundary(
#     created=datetime.datetime(2019, 6, 27, 16, 53, 5),
#     uid='flow_boundary',
#     display_name='flow_boundary',
#     location={'x': 0.0, 'y': 0.0, 'z': 0.0},
#     schematic_location={'x': 0.0, 'y': 0.0, 'z': 0.0})
# ,
# ...
# ]
```
