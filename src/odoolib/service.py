import logging

from .connector._sender import Sender


class Service(object):
    """
    A class to execute RPC calls on a specific service of the remote server.
    """

    def __init__(self, connector: Sender, service_name: str):
        """
        :param connector: A valid Connector instance.
        :param service_name: The name of the service on the remote server.
        """
        self.connector = connector
        self.service_name = service_name
        self._logger = logging.getLogger(f"{__name__}.{service_name}")

    def __getattr__(self, method: str):
        """
        :param method: The name of the method to execute on the service.
        """
        self._logger.debug("method: %r", method)

        def proxy(*args):
            """
            :param args: A list of values for the method
            """
            self._logger.debug("args (sync): %r", args)
            result = self.connector.send(self.service_name, method, *args)
            self._logger.debug("result (sync): %r", result)
            return result

        async def async_proxy(*args):
            """
            :param args: A list of values for the method
            """
            self._logger.debug("args (async): %r", args)
            result = await self.connector.async_send(self.service_name, method, *args)
            self._logger.debug("result (async): %r", result)
            return result

        # Attach `.async_` to the sync proxy for async usage
        proxy.async_ = async_proxy
        return proxy
