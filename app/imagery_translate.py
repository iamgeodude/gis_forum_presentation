import rio_cogeo
from data_stores import local_store, cloudflare_store
import morecantile

collections = local_store.get_collections()
tms = morecantile.tms.get("WGS1984Quad")

for c in collections:
    files = [
        file for file in local_store.get_collection_items(c) if ".cog.tif" in file
    ]

    for file in files:
        local_path = f"/{file}"
        web_optimized_path = f"/{file.split(".cog.tif")[0]}.cog.tif"

        print(file)
        rio_cogeo.cogeo.cog_translate(
            local_path,
            web_optimized_path,
            rio_cogeo.profiles.cog_profiles.get("deflate"),
            use_cog_driver=True,
            in_memory=False,
            forward_band_tags=True,
            forward_ns_tags=True,
            tms=tms
        )

    web_files = [
        file for file in local_store.get_collection_items(c) if ".cog.tif" in file
    ]

    for file in web_files:
        # upload web_optimized cogs to cloudflare
        local_path = f"/{file}"
        r2_key = "/".join(file.split("/")[4:])

        print(r2_key)
        with open(local_path, "rb") as content:
            print(f"uploading {local_path} to {r2_key}")
            cloudflare_store.store.put(
                r2_key, content, use_multipart=True, max_concurrency=4
            )
