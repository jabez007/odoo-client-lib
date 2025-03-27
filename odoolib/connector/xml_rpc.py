import logging
from xmlrpc.client import ServerProxy

from ._connector import Connector


class XmlRpcConnector(Connector):
    """
    A type of connector that uses the XMLRPC protocol.
    """

    PROTOCOL = "xmlrpc"

    def __init__(self, hostname: str, port=8069):
        """
        Initialize by specifying the hostname and the port.
        :param hostname: The hostname of the computer holding the instance of Odoo.
        :param port: The port used by the Odoo instance for XMLRPC (default to 8069).
        """
        super().__init__()
        self._logger = logging.getLogger(f"{self._logger.name}.xmlrpc")
        self.url = "http://%s:%d/xmlrpc" % (hostname, port)

    def send(self, service_name: str, method: str, *args):
        url = "%s/%s" % (self.url, service_name)
        service = ServerProxy(url)
        return getattr(service, method)(*args)
