from util import CngStore

# remote store destination settings
# cloudflare settings
cloudflare_r2_url = "https://b7d81081da49507103148725964b31ac.r2.cloudflarestorage.com"
cloudflare_r2_cng_bucket_public_url = (
    "https://stac.iamgeodude.com/"
)
cloudflare_r2_prefix = (
    "STAC_CNG/c/stratmap-2019-50cm-brown-county/resources/uncompressed/dem/"
)

cloudflare_r2_config = {
    "access_key_id": "XXXXXXXXXXXXXXXXXXX",
    "secret_access_key": "XXXXXXXXXXXXXXXXXXX",
    "endpoint": cloudflare_r2_url,
}

OUT_BASEPATH = "/run/media/repdsk/secondary/STAC_CNG/"


local_store = CngStore(collections_prefix=f"{OUT_BASEPATH}/c/", local=True)
cloudflare_store = CngStore(
    bucket="cng", config=cloudflare_r2_config, collections_prefix="STAC_CNG/c/"
)