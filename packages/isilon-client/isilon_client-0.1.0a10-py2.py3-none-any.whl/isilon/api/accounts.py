from typing import Optional

from isilon.api.base import BaseAPI
from isilon.api.metadata import account_metadata


class Accounts(BaseAPI):
    async def show(self, account_name: str, **kwargs):
        """Show account details and list containers."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.get(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}?format=json",
            **kwargs,
        ) as resp:
            response = await resp.json()
            return response

    async def update(
        self, account_name: str, metadata: Optional[dict] = None, **kwargs
    ) -> int:
        """Create, update, or delete account metadata."""
        kwargs = await self.include_auth_header(**kwargs)
        kwargs = await self._include_account_metadata(metadata, **kwargs)
        async with self.http.post(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}",
            **kwargs,
        ) as resp:
            return resp.status

    async def metadata(self, account_name: str, **kwargs) -> dict:
        """Show account metadata."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.head(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}",
            **kwargs,
        ) as resp:
            return dict(resp.headers)

    async def _include_account_metadata(self, metadata, **kwargs) -> dict:
        if metadata:
            metadata_headers = account_metadata(metadata)
            kwargs["headers"].update(metadata_headers)
        return kwargs
