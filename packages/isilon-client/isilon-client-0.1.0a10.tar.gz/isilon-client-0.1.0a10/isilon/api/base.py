from aiohttp import ClientSession


class BaseAPI:
    API_VERSION = "v1"

    def __init__(self, client) -> None:
        self._client = client

    async def include_auth_header(self, **kwargs: dict) -> dict:
        token = await self._client.credentials.x_auth_token()
        kwargs.update({"headers": token})
        return kwargs

    @property
    def address(self) -> str:
        return self._client.address  # type: ignore

    @property
    def http(self) -> ClientSession:
        return self._client.http  # type: ignore

    @property
    def account(self) -> str:
        return self._client.account  # type: ignore

    def __repr__(self) -> str:
        *_, name = str(self.__class__).split(".")
        return f"{name[:-2]}(api_version='{self.API_VERSION}')"
