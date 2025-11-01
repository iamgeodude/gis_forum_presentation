import json
import pdal
from data_stores import (
    local_store,
)
collections = local_store.get_collections()


def lpc_to_copc(input_path, output_path):
    pipeline = [
        {"type": "readers.las", "filename": input_path},
        {"type": "writers.copc", "filename": output_path},
    ]
    pipeline_json = json.dumps(pipeline)
    pipeline = pdal.Pipeline(pipeline_json)

    pipeline.execute()

for c in collections:
    items = [item for item in local_store.get_collection_items(c) if ".laz" in item]

    for item in items:
        local_file = f"/{item}"
        new_file = item.split(".laz")[0] + ".copc.laz"

        lpc_to_copc(local_file, new_file)