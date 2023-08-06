# Kafka Connect Python Helper

## Description
This package can be used to simplify HTTP commands for the Kafka Connect REST API. The package is created spefically for deploying connectors automatically, but can also be used to simplify one-time commands.

For an example, see examples/setup_mm2.py

## Dependencies and limitations
The package heavily relies on the Requests package and is currently designed to expect that the Requests session is created upfront.

The code must still be extended to support other Connect REST commands (e.g. resume/pause and POSTs).

## Usage
Prepare the requests session and setup the helper library, for example for a Connect REST API with SASL_SSL:
```
import requests
import logging
from connect_helper import ConnectHelper

logging.basicConfig(level=logging.INFO)

username = "dummy"
password = "supersecret"
base_url = "https://localhost:8083"

s = requests.Session()
s.verify = ca_cert
s.auth = (username, password)

connect = ConnectHelper(s, base_url)

r = connect.get_connectors()
```

To get or edit a specific connector, first set the connector name:
```
connect.connector.name = "new_connector_name"
```

After that you can run connect.connector commands, e.g. to get the remote configuration or push your new configuration. See for a full example examples/setup_mm2.py:
```
print(connect.connector.get_remote_config().json())
connect.connector.put({})
connect.connector.poll_status()
```