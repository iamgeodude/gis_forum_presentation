# use conda env "vector_data"
from data_stores import cloudflare_store, local_store
import geopandas
import pystac
import shapely


def vec_to_parquet(in_path: str, out_path: str):
    #con = duckdb.connect(database=":memory:", read_only=False)
    gdf = geopandas.read_file(in_path)
    gdf.to_parquet(out_path, engine='pyarrow', write_covering_bbox=True)
    

loc_collections = local_store.get_collections()

for c in loc_collections:
    # print(c)

    items = local_store.get_collection_items(c)
    # print(items)

    hypso_files = [
        file
        for file in local_store.s3_list_objects(f"{c}/resources/uncompressed/hypso")
        if ".shp" in file
    ]

    """ for file in hypso_files:
        new_filename = f"/{file.split(".")[:-1][0]}.parquet"
        print(new_filename, file, "\n\n\n")
        vec = vec_to_parquet(f"/{file}", new_filename) """
   
    hypso_parquet_files = [
        file
        for file in local_store.s3_list_objects(f"{c}/resources/uncompressed/hypso")
        if ".parquet" in file
    ]

    for file in hypso_parquet_files:
        abs_path = f"/{file}"
        s3_path = "/".join(file.split("/")[4:])
        print(file, s3_path)

        with open(abs_path, "rb") as content:
            cloudflare_store.store.put(
                s3_path, content, use_multipart=True, max_concurrency=4
            )
       