import logging

from aiohttp import ClientSession


class HttpSender:
    def __init__(self):
        self.client = ClientSession()
        self.logger = logging.getLogger(self.__class__.__name__)

    async def send(self, addr: str, data: bytes):
        if addr != None and data != None:
            async with self.client.post(addr, data=data) as response:
                if response.status != 200:
                    self.logger.error(
                        "send failed status: %d data: %s", response.status, data
                    )
                # else:
                #     print(await response.text())

    async def close(self):
        await self.client.close()
