import json
import logging
import random

import requests

from ._connector import Connector


class JsonRpcException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


class JsonRpcConnector(Connector):
    """
    A type of connector that uses the JsonRPC protocol.
    """

    PROTOCOL = "jsonrpc"

    def __init__(self, hostname: str, port=8069):
        """
        Initialize by specifying the hostname and the port.
        :param hostname: The hostname of the computer holding the instance of Odoo.
        :param port: The port used by the Odoo instance for JsonRPC (default to 8069).
        """
        super().__init__()
        self._logger = logging.getLogger(f"{self._logger.name}.jsonrpc")
        self.url: str = "http://%s:%d/jsonrpc" % (hostname, port)

    def send(self, service_name: str, method: str, *args):
        return self._json_rpc(
            "call", {"service": service_name, "method": method, "args": args}
        )

    def _json_rpc(self, fct_name, params):
        data = {
            "jsonrpc": "2.0",
            "method": fct_name,
            "params": params,
            "id": random.randint(0, 1000000000),
        }
        result_req = requests.post(
            self.url,
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
            },
        )
        result = result_req.json()
        if result.get("error", None):
            raise JsonRpcException(result["error"])
        return result.get("result", False)
