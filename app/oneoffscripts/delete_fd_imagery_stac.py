from data_stores import cloudflare_store


stac_jsons = cloudflare_store.s3_list_objects_delimited("STAC_CNG/c/stratmap-2019-50cm-brown-county")['objects']

for obj in [obj for  obj in stac_jsons if "stratmap19-1m" in obj['path'] and ".tif." not in obj['path']]:
    print(obj['path'])
