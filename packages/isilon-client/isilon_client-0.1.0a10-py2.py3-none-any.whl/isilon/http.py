import attr
from aiohttp import ClientSession

from isilon.response import Response


@attr.s(frozen=True)
class Http:
    async def get(self, url, session_config=dict(), *args, **kwargs):
        async with ClientSession(**session_config) as session:
            response = await session.get(url, *args, **kwargs)
        return Response(response)

    async def get_large_object(
        self, url, filename, chunk_size=50, session_config=dict(), *args, **kwargs
    ):
        async with ClientSession(**session_config) as session:
            response = await session.get(url, *args, **kwargs)
            with open(filename, "wb") as f:
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
        return Response(response)

    async def post(self, url, session_config=dict(), *args, **kwargs):
        async with ClientSession(**session_config) as session:
            response = await session.post(url, *args, **kwargs)
        return Response(response)

    async def send_large_object(
        self, url, filename, session_config=dict(), *args, **kwargs
    ):
        with open(filename, "rb") as f:
            response = await self.put(
                url, session_config=session_config, data=f, *args, **kwargs
            )
        return Response(response)

    async def put(self, url, session_config=dict(), *args, **kwargs):
        async with ClientSession(**session_config) as session:
            response = await session.put(url, *args, **kwargs)
        return Response(response)

    async def delete(self, url, session_config=dict(), *args, **kwargs):
        async with ClientSession(**session_config) as session:
            response = await session.delete(url, *args, **kwargs)
        return Response(response)

    async def head(self, url, session_config=dict(), *args, **kwargs):
        async with ClientSession(**session_config) as session:
            response = await session.head(url, *args, **kwargs)
        return Response(response)
