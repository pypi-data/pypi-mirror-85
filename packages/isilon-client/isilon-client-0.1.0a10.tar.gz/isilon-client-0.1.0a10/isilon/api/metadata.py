from functools import partial


def metadata_build(prefix: str, metadata: dict) -> dict:
    return {f"{prefix}-{name.capitalize()}": value for name, value in metadata.items()}


object_metadata = partial(metadata_build, "X-Object-Meta")
container_metadata = partial(metadata_build, "X-Container-Meta")
account_metadata = partial(metadata_build, "X-Account-Meta")
