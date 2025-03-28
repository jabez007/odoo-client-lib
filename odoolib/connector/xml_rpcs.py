import logging
from typing import Optional
from xmlrpc.client import SafeTransport

from .xml_rpc import XmlRpcConnector


class XmlRpcsConnector(XmlRpcConnector):
    """
    A type of connector that uses the secured XMLRPC protocol.
    """

    PROTOCOL = "xmlrpcs"

    def __init__(
        self,
        hostname: str,
        port=8069,
        version: Optional[str] = "2",
        transport: Optional[SafeTransport] = None,
    ):
        super(XmlRpcsConnector, self).__init__(hostname, port, version, transport)
        self._logger = logging.getLogger(
            f"{str.join('.', self._logger.name.split('.')[:-1])}.xmlrpcs"
        )
        self.url = (
            "https://%s:%d/xmlrpc" % (hostname, port)
            if version is None
            else "https://%s:%d/xmlrpc/%s" % (hostname, port, version)
        )
