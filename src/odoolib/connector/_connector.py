import logging
from typing import Optional

from ..service import Service
from ._sender import Sender


class Connector(Sender):
    """
    The base abstract class representing a connection to an Odoo Server.
    """

    def __init__(self):
        self._logger = logging.getLogger(f"{str.join('.', __name__.split('.')[:-1])}")
        self.url: Optional[str] = None

    def get_service(self, service_name: str) -> Service:
        """
        Returns a Service instance to allow easy manipulation of one of the services offered by the remote server.

        :param service_name: The name of the service.
        """
        return Service(self, service_name)
