from typing import Optional

from isilon.api.base import BaseAPI
from isilon.api.metadata import object_metadata


class Objects(BaseAPI):
    async def get(
        self,
        container_name: str,
        object_name: str,
        **kwargs,
    ) -> bytes:
        """Get object content and metadata."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.get(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}/{object_name}",
            **kwargs,
        ) as resp:
            content: bytes = await resp.content.read()
            return content

    async def get_large(
        self,
        container_name: str,
        object_name: str,
        filename: str,
        chunk_size: int = 50,
        **kwargs,
    ) -> int:
        """Get large object content and metadata."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.get(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}/{object_name}",
            **kwargs,
        ) as resp:
            with open(filename, "w+b") as f:
                while True:
                    chunk = await resp.content.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
            return resp.status

    async def create(
        self,
        container_name: str,
        object_name: str,
        data,
        metadata: Optional[dict] = None,
        **kwargs,
    ) -> int:
        """Create or replace object."""
        kwargs = await self.include_auth_header(**kwargs)
        kwargs = await self._include_object_metadata(metadata, **kwargs)
        async with self.http.put(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}/{object_name}",
            data=data,
            **kwargs,
        ) as resp:
            return resp.status

    async def create_large(
        self,
        container_name: str,
        object_name: str,
        filename: str,
        metadata: Optional[dict] = None,
        **kwargs,
    ) -> int:
        """Create or replace large object."""
        kwargs = await self.include_auth_header(**kwargs)
        kwargs = await self._include_object_metadata(metadata, **kwargs)
        with open(filename, "rb") as f:
            async with self.http.put(
                f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}/{object_name}",
                data=f,
                **kwargs,
            ) as resp:
                return resp.status

    async def copy(self, container_name, object_name, **kwargs):
        """Copy object."""
        raise NotImplementedError("Operation not supported")

    async def delete(self, container_name: str, object_name, **kwargs) -> int:
        """Delete object."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.delete(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}/{object_name}",
            **kwargs,
        ) as resp:
            return resp.status

    async def show_metadata(
        self, container_name: str, object_name: str, **kwargs
    ) -> dict:
        """Show object metadata."""
        kwargs = await self.include_auth_header(**kwargs)
        async with self.http.head(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}/{object_name}",
            **kwargs,
        ) as resp:
            return dict(resp.headers)

    async def update_metadata(
        self,
        container_name: str,
        object_name: str,
        metadata: Optional[dict] = None,
        **kwargs,
    ) -> int:
        """Create or update object metadata."""
        kwargs = await self.include_auth_header(**kwargs)
        kwargs = await self._include_object_metadata(metadata, **kwargs)
        async with self.http.post(
            f"{self.address}/{self.API_VERSION}/AUTH_{self.account}/{container_name}/{object_name}",
            **kwargs,
        ) as resp:
            return resp.status

    async def _include_object_metadata(self, metadata, **kwargs) -> dict:
        if metadata:
            metadata_headers = object_metadata(metadata)
            kwargs["headers"].update(metadata_headers)
        return kwargs
