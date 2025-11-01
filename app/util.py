from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from obstore.store import S3Config
from obstore.store import (
    S3Store,
    LocalStore,
)


class CngStore:
    store: S3Store | LocalStore | None
    bucket: str = "cng"
    collections_prefix: str = ""
    config: S3Config
    local: bool = False

    def __init__(
        self,
        bucket: str | None = None,
        collections_prefix: str = "",
        config: S3Config | None = None,
        local: bool = False,
    ):
        self.local = local
        self.bucket = bucket
        self.collections_prefix = collections_prefix

        if not local:
            self.store = S3Store(
                bucket=bucket,
                config=config,
            )
        else:
            self.store = LocalStore(mkdir=True, automatic_cleanup=True)

    def s3_sync_upload(self, local_path: str, remote_path: str):
        with open(local_path, "rb") as content:
            self.put(remote_path, content, use_multipart=True, max_concurrency=4)

    def s3_list_objects(self, prefix: str):
        stream = self.store.list(prefix=prefix)
        contents = [meta["path"] for batch in stream for meta in batch]
        return contents

    def s3_list_objects_delimited(self, prefix: str | None = ""):
        stream = self.store.list_with_delimiter(prefix=prefix, return_arrow=False)

        return stream

    def get_collections(self):
        res = self.s3_list_objects_delimited(prefix=self.collections_prefix)
        return res["common_prefixes"]

    def get_collection_items(self, collection_path: str):
        stream = self.s3_list_objects(f"{collection_path}/resources/")

        return stream

    def get_collection_assets(self, collection_path: str):
        stream = self.s3_list_objects(f"{collection_path}/assets/")

        contents = stream

        return contents
