from data_stores import cloudflare_r2_cng_bucket_public_url, cloudflare_store
import json
from datetime import datetime
import geopandas
import pystac
from pystac.layout import TemplateLayoutStrategy
from shapely.geometry import mapping, box
from shapely import to_geojson
from collections.abc import Iterable


def parquet_to_stac_item(
    vector_file_path: str, stac_collection: pystac.Collection
) -> pystac.Item:
    # Item Meta
    item_id = vector_file_path.split("/")[-1]
    r2_public_url_collection_path = stac_collection.self_href.split("collection.json")[0]
    stac_item_json_url = f"{r2_public_url_collection_path}{item_id}.json"
    public_asset_url = f"{cloudflare_r2_cng_bucket_public_url}{vector_file_path}"
    r2_asset_key = f"s3://cng/{vector_file_path}"
    asset_media_type = pystac.MediaType.PARQUET

    gdf = geopandas.read_parquet(r2_asset_key).to_crs(4326)

    #geometry = mapping(gdf.union_all())
    bbox = list(gdf.total_bounds)
    geometry = mapping(box(*bbox))
    item_datetime = datetime(2019, 3, 8)
    properties = {}

    stac_item = pystac.Item(
        id=item_id,
        geometry=geometry,
        bbox=bbox,
        datetime=item_datetime,
        href=stac_item_json_url,
        collection=stac_collection,
        properties=properties,
    )
    stac_asset = pystac.Asset(
        href=public_asset_url,
        title="hypsography",
        description="A geoparquet file containing the derived hypsography geometries",
        roles=["data", "HYPSO"],
        media_type=asset_media_type
    )

    stac_item.add_asset("hypsography", stac_asset)

    return stac_item

collections = cloudflare_store.get_collections()
for c in collections:
    collection_url = f"{cloudflare_r2_cng_bucket_public_url}{c}/collection.json"

    vectors = [
        vec for vec in cloudflare_store.get_collection_items(c) if ".parquet" in vec
    ]

    collection = pystac.Collection.from_file(collection_url)
    collection.catalog_type = pystac.CatalogType.ABSOLUTE_PUBLISHED

    new_items: Iterable[pystac.Item] = []

    for vec in vectors:
        item_id = vec.split("/")[-1]
        stac_item_json_url = f"{cloudflare_r2_cng_bucket_public_url}{c}/{item_id}.json"
        stac_item_key = stac_item_json_url.split(cloudflare_r2_cng_bucket_public_url)[-1]
        ## upload stac item info
        stac_item_json_r2_key = f"{c}/{item_id}.json"

        print("Generating STAC Item...")
        stac_item = parquet_to_stac_item(vec, collection)

        print("Validating generated STAC Item...")
        validations = stac_item.validate()
        print(validations, stac_item.self_href)

        print("Uploading STAC Item JSON to remote...")
        stac_item_bytes = json.dumps(stac_item.to_dict(transform_hrefs=False)).encode("utf-8")
        cloudflare_store.store.put(stac_item_key, stac_item_bytes)

        # set template strategy so that item hrefs in collection do not get f'd up
        strategy = TemplateLayoutStrategy(item_template=stac_item.self_href)
        collection.add_item(stac_item, strategy=strategy, set_parent=False)

    # update collection stac json
    new_coll_bytes = json.dumps(collection.to_dict(transform_hrefs=False)).encode("utf-8")
    cloudflare_store.store.put(f"{c}/collection.json", new_coll_bytes)