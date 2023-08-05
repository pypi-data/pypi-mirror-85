from isilon.api.base import BaseAPI


class Discoverability(BaseAPI):
    async def info(self, **kwargs):
        """List activated capabilities."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.get(f"{self.address}/info", **kwargs) as resp:
            json_response = await resp.json()
        return json_response
