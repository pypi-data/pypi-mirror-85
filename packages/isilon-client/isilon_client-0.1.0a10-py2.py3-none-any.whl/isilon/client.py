import asyncio
import os

import attr
from aiohttp import ClientSession

from isilon.api import Accounts, Containers, Discoverability, Endpoints, Objects
from isilon.creds import Credentials


@attr.s
class IsilonClient:
    address = attr.ib(
        type=str,
        default=os.getenv("ISILON_ADDRESS", "http://localhost:8080"),
        validator=attr.validators.instance_of(str),
    )
    account = attr.ib(
        type=str,
        default=os.getenv("ISILON_ACCOUNT", "test"),
        validator=attr.validators.instance_of(str),
    )
    user = attr.ib(
        type=str,
        default=os.getenv("ISILON_USER", "tester"),
        validator=attr.validators.instance_of(str),
    )
    password = attr.ib(
        type=str,
        default=os.getenv("ISILON_PASSWORD", "testing"),
        validator=attr.validators.instance_of(str),
    )
    http = attr.ib(
        type=ClientSession,
        factory=ClientSession,
        validator=attr.validators.instance_of(ClientSession),
        repr=False,
    )

    def __attrs_post_init__(self) -> None:
        self.credentials = Credentials(self)
        self.discoverability = Discoverability(self)
        self.objects = Objects(self)
        self.containers = Containers(self)
        self.endpoints = Endpoints(self)
        self.accounts = Accounts(self)

    def _loop(self):
        try:
            loop = asyncio.get_running_loop()
        except AttributeError:
            loop = asyncio._get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
        return loop

    def __del__(self) -> None:
        if not self.http.closed:
            self._loop().run_until_complete(self.http.close())


async def init_isilon_client(*args, **kwargs) -> IsilonClient:
    return IsilonClient(*args, **kwargs)
