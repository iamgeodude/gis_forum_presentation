import json
import pystac
from pystac.layout import TemplateLayoutStrategy
import subprocess
from data_stores import cloudflare_store, cloudflare_r2_cng_bucket_public_url


def get_pdal_info_stac(laz_path: str) -> pystac.Item:
    cmd = f"pdal info --stac {laz_path}"
    cmd_array = cmd.split(" ")

    process = subprocess.run(cmd_array, capture_output=True, text=True, check=True)
    json_txt = process.stdout
    if process.stderr:
        # print(process.stderr)
        pass

    result_json = json.loads(json_txt)
    stac_item_dict = result_json["stac"]
    stupid_local_path = "/home/repdsk/code/python/gis_forum_presentation/"

    for link in stac_item_dict["links"]:
        cur_href = link["href"]
        new_href = cur_href.replace(stupid_local_path, "")
        link["href"] = new_href

    for asset_key in stac_item_dict["assets"]:
        cur_href = stac_item_dict["assets"][asset_key]["href"]
        new_href = cur_href.replace(stupid_local_path, "")
        stac_item_dict["assets"][asset_key]["href"] = new_href

    stac_item = pystac.Item.from_dict(stac_item_dict)

    return stac_item


catalog_url = f"{cloudflare_r2_cng_bucket_public_url}STAC_CNG/c/catalog.json"
catalog = pystac.Catalog.from_file(catalog_url)
collections = cloudflare_store.get_collections()

for c in collections:
    collection_url = f"{cloudflare_r2_cng_bucket_public_url}{c}/collection.json"
    collection = pystac.Collection.from_file(collection_url)
    # print(catalog.to_dict(), collection.to_dict())
    items = cloudflare_store.get_collection_items(c)

    for item in [item for item in items if ".copc.laz" in item][:1]:
        public_asset_url = f"{cloudflare_r2_cng_bucket_public_url}{item}"
        item_id = item.split("/")[-1]
        stac_item_json_url = f"{cloudflare_r2_cng_bucket_public_url}{c}/{item_id}.json"
        stac_item_key = stac_item_json_url.split(cloudflare_r2_cng_bucket_public_url)[
            -1
        ]

        stac_item = get_pdal_info_stac(public_asset_url)
        stac_item.id = item_id
        stac_item.set_self_href(stac_item_json_url)
        stac_item.set_collection(collection=collection)

        #print(json.dumps(stac_item.to_dict()))

        print("Validating generated STAC Item...")
        validations = stac_item.validate()
        #print(validations, stac_item.self_href)

        print("Uploading STAC Item JSON to remote...")
        stac_item_bytes = json.dumps(stac_item.to_dict(transform_hrefs=False)).encode("utf-8")
        #cloudflare_store.store.put(stac_item_key, stac_item_bytes)
        strategy = TemplateLayoutStrategy(item_template=stac_item.self_href)

        collection.add_item(stac_item, strategy=strategy, set_parent=False)

    # update collection stac json
    print("\n\n", json.dumps(collection.to_dict(transform_hrefs=False)))
    new_coll_bytes = json.dumps(collection.to_dict(transform_hrefs=False)).encode(
        "utf-8"
    )
    #cloudflare_store.store.put(f"{c}/collection.json", new_coll_bytes)


#### pick this shit back up... youre done for the night