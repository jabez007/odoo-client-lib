import asyncio
import logging
from typing import Any, Optional

from ..service import Service


class Connector(object):
    """
    The base abstract class representing a connection to an Odoo Server.
    """

    PROTOCOL: Optional[str] = None

    def __init__(self):
        self._logger = logging.getLogger(f"{str.join('.', __name__.split('.')[:-1])}")
        self.url: Optional[str] = None

    def get_service(self, service_name: str):
        """
        Returns a Service instance to allow easy manipulation of one of the services offered by the remote server.

        :param service_name: The name of the service.
        """
        return Service(self, service_name)

    def send(self, service_name: str, method: str, *args) -> Any:
        """
        stub out method for children to override
        """
        return {"service_name": service_name, "method": method, "args": args}

    async def async_send(self, service_name: str, method: str, *args) -> Any:
        """
        Async wrapper around `send` to allow non-blocking execution.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, lambda: self.send(service_name, method, *args)
        )
