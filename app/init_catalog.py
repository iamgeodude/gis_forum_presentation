import pystac
from pystac.layout import TemplateLayoutStrategy
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

collections = cloudflare_store.get_collections()

for c in collections:
    print(collections)
    collection_id = c.split("/")[-1]
    collection_url = f"{cloudflare_r2_cng_bucket_public_url}{c}/collection.json"
    collection_stac_json_r2_key = f"{c}/collection.json"

    collection = pystac.Collection(
        id=collection_id,
        title=collection_id,
        description="This StratMap lidar project covers a portion of Brown County around Brownwood, Texas. This project was managed by the Texas Strategic Mapping (StratMap) Program and utilized the StratMap contracts held by the Department of Information Resources (DIR). Collection took place March 7-8, 2019. Data was collected and processed by the Sanborn Mapping Company, LLC with third party quality assurance/quality control performed by AECOM. \r\n\r\nThe StratMap contributing partner for this project was the Texas Commission on Environmental Quality (TCEQ). Lidar acquired from this project will be used for floodplain management and planning, feature extraction, water quality modeling, stream restoration potential analysis, change detection, 9-1-1, wildfire mitigation, habitat identification/modeling for endangered species, and dam safety.\r\n\r\nPoints are classified based on the following classifications. \r\n\r\nClass 1: Unclassified\r\nClass 2: Ground\r\nClass 3: Low vegetation\r\nClass 4: Medium vegetation\r\nClass 5: Tall vegetation\r\nClass 6: Buildings\r\nClass 7: Low Point (noise)\r\nClass 9: Water\r\nClass 10: Ignored Ground\r\nClass 14: Culverts\r\nClass 17: Bridges\r\n\r\nLidar-derived multipatch buildings and footprints were prepared as an estimate for a state-wide inventory of buildings. This may or may not accurately reflect the actual value/boundaries of a particular building but is an approximation of reality. Use at your own discretion.",
        keywords=[
            "category:elevation",
            "category:lidar",
            "file_type:COPC.LAZ",
            "file_type:PARQUET",
            "file_type:COG.TIFF",
            "resource_type:DEM",
            "resource_type:HYPSO",
            "resource_type:LPC",
            "data_type:raster",
            "data_type:vector",
            "data_type:3D",
        ],
        extent=pystac.Extent(
            spatial=pystac.SpatialExtent(
                [
                    [
                        -99.07867149990825,
                        31.60891336113745,
                        -98.74943620441208,
                        31.875467815893497,
                    ]
                ]
            ),
            temporal=pystac.TemporalExtent([datetime(2019, 3, 8), None]),
        ),
        href=collection_url,
    )

catalog_json_text = json.dumps(catalog.to_dict(), indent=4)
catalog_json_bytes = catalog_json_text.encode("utf-8")
collection_json_text = json.dumps(collection.to_dict(), indent=4)
collection_json_bytes = collection_json_text.encode("utf-8")

print(catalog_json_text)
print(collection_json_text)

cloudflare_store.store.put(catalog_stac_json_r2_key, catalog_json_bytes)
cloudflare_store.store.put(collection_stac_json_r2_key, collection_json_bytes)
