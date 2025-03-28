import logging
from typing import Optional

from .json_rpc import JsonRpcConnector


class JsonRpcsConnector(JsonRpcConnector):
    """
    A type of connector that uses the JsonRPC protocol.
    """

    PROTOCOL = "jsonrpcs"

    def __init__(self, hostname, port=8069, version: Optional[str] = "2"):
        """
        Initialize by specifying the hostname and the port.
        :param hostname: The hostname of the computer holding the instance of Odoo.
        :param port: The port used by the Odoo instance for JsonRPC (default to 8069).
        """
        super(JsonRpcsConnector, self).__init__(hostname, port)
        self._logger = logging.getLogger(
            f"{str.join('.', self._logger.name.split('.')[:-1])}.jsonrpcs"
        )
        self.url = (
            "https://%s:%d/jsonrpc" % (hostname, port)
            if version is None
            else "https://%s:%d/jsonrpc/%s" % (hostname, port, version)
        )
