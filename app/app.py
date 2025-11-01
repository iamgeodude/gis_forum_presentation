from obstore.store import S3Store
import asyncio
import json
import logging
import os

# import pdal
# from osgeo import gdal

# remote store source settings
# txgio remote bucket settings
bucketname = "test-gio-data-warehouse"
region_name = "us-east-1"
txgio_s3_directory_prefix = (
    "c/stratmap-2019-50cm-brown-county/resources/uncompressed/dem/"
)

txgio_store = S3Store.from_url(
    f"s3://{bucketname}", region=region_name, skip_signature=True
)


# remote store destination settings
# cloudflare settings
cloudflare_account = "b7d81081da49507103148725964b31ac"
cloudflare_bucket = "cng"
cloudflare_r2_url = (
    "https://b7d81081da49507103148725964b31ac.r2.cloudflarestorage.com/cng/"
)
cloudflare_r2_cng_bucket_public_url = (
    "https://pub-e3407793dbf7498db1594ad32173f565.r2.dev/"
)
cloudflare_r2_prefix = (
    "STAC_CNG/c/stratmap-2019-50cm-brown-county/resources/uncompressed/dem/"
)
cloudflare_store = S3Store.from_url(
    cloudflare_r2_url,
    access_key_id="c899ffa55432cb8a57c3590e225e4f68",
    secret_access_key="df8b19e550258621e450c352efefbc3393d5f4da01f5d0caf28f77b2c77878cf",
)

# local settings
OUT_BASEPATH = "/run/media/repdsk/secondary/STAC_CNG/"

# configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)

logger = logging.getLogger(__name__)


def list_s3_contents(store: S3Store, prefix: str):
    results = store.list(prefix=prefix)

    return results


def download_s3_object(store: S3Store, prefix: str, write_path: str):
    write_dir = os.path.split(write_path)[0]

    logger.info(f"Getting s3 object with prefix {prefix}.")
    resp = store.get(prefix)

    logger.info(f"Creating directory {write_dir} if not exists.")
    os.makedirs(write_dir, exist_ok=True)

    logger.info(f"Writing file to {write_path}.")
    with open(write_path, "wb") as f:
        for chunk in resp:
            f.write(chunk)


def get_files_in_dir(dir: str):
    logger.info(f"Getting files in directory '{dir}'.")
    return [dir + file for file in os.listdir(dir) if os.path.isfile(dir + file)]


def get_non_copc_lazfiles_in_dir(dir):
    logger.info("Getting non copc .laz files in directory {dir}.")
    unfiltered = get_files_in_dir(dir)
    return [
        file
        for file in unfiltered
        if "COPC" not in file and "copc" not in file and ".laz" in file
    ]


def get_copc_lazfiles_in_dir(dir: str):
    logger.info("Getting copc files in directory {dir}.")
    unfiltered = get_files_in_dir(dir)
    return [
        file
        for file in unfiltered
        if ("COPC" in file or "copc" in file) and ".laz" in file
    ]


def laz_to_copc(laz_path: str):
    split_path = os.path.split(laz_path)
    copc_file_name = split_path[1].split(".")[0] + "_COPC.laz"
    copc_output_path = split_path[0] + "/" + copc_file_name

    if os.path.exists(copc_output_path):
        print(f"{copc_output_path} already exists. Skipping.")
        return

    pipeline = [
        {"type": "readers.las", "filename": laz_path},
        {"type": "writers.copc", "filename": copc_output_path},
    ]
    pipeline_json = json.dumps(pipeline)
    pipeline = pdal.Pipeline(pipeline_json)

    logger.info(f"Creating COPC file {copc_output_path}.")
    pipeline.execute()

    logger.info(f"COPC file '{copc_output_path}' created successfully.")


def get_raster_files_in_dir(dir: str):
    RASTER_TYPES = [
        "img",
        "IMG",
        "jpeg",
        "JPEG",
        "jpg",
        "JPG",
        "JPEG2000",
        "JPG2000",
        "png",
        "PNG",
        "tif",
        "TIF",
        "TIFF",
    ]
    logger.info("Getting raster files in directory {dir}.")
    unfiltered = get_files_in_dir(dir)

    return [file for file in unfiltered if file.split(".")[-1] in RASTER_TYPES]


def raster_to_cog(input_path: str):
    split_path = os.path.split(input_path)
    raster_file_name = split_path[1].split(".")[0] + "_COG.tif"
    raster = gdal.Open(input_path)
    output_dir = split_path[0]
    output_path = output_dir + "/" + raster_file_name

    if raster is None:
        logger.error(f"Error: could not open {input_path}.")

        return

    creation_options = [
        "COMPRESS=LZW",
        "PREDICTOR=2",
        "NUM_THREADS=ALL_CPUS",
        "BIGTIFF=YES",
    ]

    logger.info(f"Converting {input_path} to COG at {output_path}.")
    gdal.Translate(output_path, raster, creationOptions=creation_options)

    raster = None

    logger.info(f"Successfully onverted {input_path} to COG at {output_path}.")


async def async_upload(local_path: str, remote_path: str):
    with open(local_path, "rb") as content:
        await cloudflare_store.put_async(
            remote_path, content, use_multipart=True, max_concurrency=4
        )


def sync_upload(local_path: str, remote_path: str):
    with open(local_path, "rb") as content:
        cloudflare_store.put(
            remote_path, content, use_multipart=True, max_concurrency=4
        )


""" laz_files = get_non_copc_lazfiles_in_dir(OUT_BASEPATH + txgio_s3_directory_prefix)
for laz_path in laz_files:
    laz_to_copc(laz_path=laz_path) """


def pdal_info_stac(laz_path, write_path: str):
    pipeline_json = json.dumps(
        {"pipeline": [{"type": "readers.las", "filename": f'"/vsicurl/{laz_path}"'}]}
    )

    pipeline = pdal.Pipeline(pipeline_json)

    pipeline.execute()

    print(pipeline.metadata, "\n\n\n", pipeline.schema)


import rio_cogeo


async def main():
    """copc_files = get_copc_lazfiles_in_dir(OUT_BASEPATH + txgio_s3_directory_prefix)

    for file, idx in copc_files:
        remote_path = cloudflare_r2_prefix + os.path.split(file)[1]
        logger.info(
            f"@ Uploading {file} to {remote_path} | ({idx}/{len(copc_files)}) @"
        )
        sync_upload(file, remote_path)"""

    """ stream = list_s3_contents(txgio_store, txgio_s3_directory_prefix)
    items = [meta["path"] for batch in stream for meta in batch]
    """
    # pdal_info_stac(f"{cloudflare_r2_cng_bucket_public_url}{items[0]}", "")

    """ with open("items.txt", "w") as file:
        for item in items:
            print(item)
            file.write(f"{cloudflare_r2_cng_bucket_public_url}{item}\n") """

    """ for item in items:
        print(item)
        download_s3_object(txgio_store, item, OUT_BASEPATH + item) """

    # get locally downloaded raster files
    files = get_raster_files_in_dir(f"{OUT_BASEPATH}{txgio_s3_directory_prefix}")
    """ for file in files:
        print(file)
        rio_cogeo.cogeo.cog_translate(
            file,
            f"{file.split("_COG.tif")[0]}.cog.tif",
            rio_cogeo.profiles.cog_profiles.get("deflate"),
            use_cog_driver=True,
            in_memory=False,
        ) """
    # upload raster files to cloudflare
    for idx, file in enumerate(files):
        remote_path = cloudflare_r2_prefix + os.path.split(file)[1]
        logger.info(
            f"@ Uploading {file} to {remote_path} | ({idx}/{len(files)}) @"
        )
        sync_upload(file, remote_path)


if __name__ == "__main__":
    asyncio.run(main())
