from isilon.api.base import BaseAPI


class Endpoints(BaseAPI):
    async def __call__(self, **kwargs) -> str:
        """List endpoints."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.get(
            f"{self.address}/{self.API_VERSION}/endpoints",
            **kwargs,
        ) as resp:
            body = await resp.text()
            return body
