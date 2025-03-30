import asyncio
from typing import Any, Optional


class Sender(object):
    """
    The base abstract class for sending RPC requests
    """

    PROTOCOL: Optional[str] = None

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
