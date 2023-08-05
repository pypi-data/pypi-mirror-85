import asyncio

from isilon.client import init_isilon_client


class Operator:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.client = self.loop.run_until_complete(init_isilon_client())

    def execute(self, command, *args, **kwargs):
        resp = self.loop.run_until_complete(command(*args, **kwargs))
        return resp
