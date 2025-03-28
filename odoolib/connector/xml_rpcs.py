import logging
from typing import Optional

from .xml_rpc import XmlRpcConnector


class XmlRpcsConnector(XmlRpcConnector):
    """
    A type of connector that uses the secured XMLRPC protocol.
    """

    PROTOCOL = "xmlrpcs"

    def __init__(self, hostname, port=8069, version: Optional[str] = "2"):
        super(XmlRpcsConnector, self).__init__(hostname, port)
        self._logger = logging.getLogger(
            f"{str.join('.', self._logger.name.split('.')[:-1])}.xmlrpcs"
        )
        self.url = (
            "https://%s:%d/xmlrpc" % (hostname, port)
            if version is None
            else "https://%s:%d/xmlrpc/%s" % (hostname, port, version)
        )
