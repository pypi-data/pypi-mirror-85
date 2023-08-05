from typing import Optional

from isilon.api.base import BaseAPI
from isilon.api.metadata import container_metadata


class Containers(BaseAPI):
    async def objects(self, container_name: str, **kwargs):
        """Show container details and list objects."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.get(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}?format=json",
            **kwargs,
        ) as resp:
            response = await resp.json()
        return response

    async def create(
        self, container_name: str, metadata: Optional[dict] = None, **kwargs
    ) -> int:
        """Create container."""
        kwargs = await self.include_auth_header(**kwargs)
        kwargs = await self._include_container_metadata(metadata, **kwargs)
        async with self.http.put(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}",
            **kwargs,
        ) as resp:
            return resp.status

    async def update_metadata(
        self, container_name: str, metadata: Optional[dict] = None, **kwargs
    ) -> int:
        """Create, update, or delete container metadata."""
        kwargs = await self.include_auth_header(**kwargs)
        kwargs = await self._include_container_metadata(metadata, **kwargs)
        async with self.http.put(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}",
            **kwargs,
        ) as resp:
            return resp.status

    async def show_metadata(self, container_name: str, **kwargs) -> dict:
        """Show container metadata."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.head(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}",
            **kwargs,
        ) as resp:
            return dict(resp.headers)

    async def delete(self, container_name: str, **kwargs) -> int:
        """Delete container."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.delete(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}",
            **kwargs,
        ) as resp:
            return resp.status

    async def _include_container_metadata(self, metadata, **kwargs) -> dict:
        if metadata:
            metadata_headers = container_metadata(metadata)
            kwargs["headers"].update(metadata_headers)
        return kwargs
