import os
import pystac
from pystac.layout import TemplateLayoutStrategy
import rio_stac
from rio_cogeo.cogeo import cog_validate
from data_stores import (
    local_store,
    cloudflare_store,
    cloudflare_r2_cng_bucket_public_url,
    cloudflare_r2_url,
)
from datetime import datetime
import json

catalog_stac_json_r2_key = f"STAC_CNG/c/catalog.json"
catalog_stac_json_public_url = (
    f"{cloudflare_r2_cng_bucket_public_url}STAC_CNG/c/catalog.json"
)
catalog = pystac.Catalog(
    id="txgio-cng-stac",
    description="A test catalog of TxGIO data translated to Cloud Native Geospatial formats.",
    title="txgio-cng-stac",
    href=catalog_stac_json_public_url,
    catalog_type=pystac.CatalogType.ABSOLUTE_PUBLISHED,
)

catalog = pystac.Catalog.from_file(catalog_stac_json_public_url)
print(catalog.to_dict())
collections = cloudflare_store.get_collections()

for c in collections:
    print(collections)
    collection_id = c.split("/")[-1]
    collection_url = f"{cloudflare_r2_cng_bucket_public_url}{c}/collection.json"
    collection_stac_json_r2_key = f"{c}/collection.json"

    collection = pystac.Collection.from_file(collection_url)

    dems = [
        dem for dem in cloudflare_store.get_collection_items(c) if ".cog.tif" in dem
    ]

    for dem in dems:
        item_id = dem.split("/")[-1]
        stac_item_json_url = f"{cloudflare_r2_cng_bucket_public_url}{c}/{item_id}.json"
        public_asset_url = f"{cloudflare_r2_cng_bucket_public_url}{dem}"
        asset_media_type = pystac.MediaType.COG
        ## upload stac item info
        stac_item_json_r2_key = f"{c}/{item_id}.json"

        print(dem)
        # create stac item from file in r2
        r2_stac_item = rio_stac.create_stac_item(
            id=item_id,
            collection=collection_id,
            collection_url=collection_url,
            source=public_asset_url,
            asset_href=public_asset_url,
            asset_name="digital elevation model",
            asset_roles=["data", "DEM"],
            asset_media_type=asset_media_type,
            with_proj=True,
            with_raster=True,
        )
        r2_stac_item.set_self_href(stac_item_json_url)
        r2_stac_item.set_collection(collection)
        r2_stac_item.set_parent(collection)
        r2_stac_item.set_root(catalog)
        strategy = TemplateLayoutStrategy(item_template=r2_stac_item.self_href)

        collection.add_item(r2_stac_item, strategy=strategy, set_parent=False)

        print(r2_stac_item.to_dict())

        item_json_string = json.dumps(r2_stac_item.to_dict(), indent=4)
        item_json_bytes = item_json_string.encode("utf-8")
        cloudflare_store.store.put(stac_item_json_r2_key, item_json_bytes)

    collection_link = catalog.add_child(collection, collection_id)

    catalog_json_text = json.dumps(catalog.to_dict(), indent=4)
    catalog_json_bytes = catalog_json_text.encode("utf-8")
    collection_json_text = json.dumps(collection.to_dict(), indent=4)
    collection_json_bytes = collection_json_text.encode("utf-8")

    print(catalog_json_text)
    print(collection_json_text)
    
    cloudflare_store.store.put(catalog_stac_json_r2_key, catalog_json_bytes)
    cloudflare_store.store.put(collection_stac_json_r2_key, collection_json_bytes)


### NOTES

# loop thru parquet and copc and create stac assets on existing tile items
# figure out what is wrong with tiffs in radiantearth browser
## perhaps content disposition? does filename need to be tiff, not tif? tiling messed up in file?

# load stac into stac-geoparquet
# add and upload stac geoparquet to s3 <collection>/assets
## start up stac-fastapi-geoparquet
## test deploying stac-fastapi-geoparquet to cloudflare workers
