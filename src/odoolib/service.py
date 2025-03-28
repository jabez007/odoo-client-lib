import asyncio
import logging


class Service(object):
    """
    A class to execute RPC calls on a specific service of the remote server.
    """

    def __init__(self, connector, service_name: str):
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

        async def proxy(*args):
            """
            Dual-purpose proxy that can handle both sync and async calls.
            :param args: A list of values for the method
            """
            self._logger.debug("args: %r", args)

            if asyncio.iscoroutinefunction(asyncio.current_task):
                # called when await was used -> await service.some_method(123)
                self._logger.debug("using async send")
                result = await self.connector.async_send(
                    self.service_name, method, *args
                )
            else:
                self._logger.debug("using send")
                result = self.connector.send(self.service_name, method, *args)

            self._logger.debug("result: %r", result)
            return result

        return proxy
