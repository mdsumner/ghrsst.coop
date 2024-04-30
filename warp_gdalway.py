
from osgeo import gdal
gdal.UseExceptions()
import os
import datetime
import random

#headers = {"Authorization": f"Bearer {os.environ['EARTHDATA_TOKEN']}"}
header = f"Authorization: Bearer {os.environ['EARTHDATA_TOKEN']}"
gdal.SetConfigOption("GDAL_HTTP_HEADERS", header)
gdal.SetConfigOption("GDAL_CACHEMAX", "2048")

def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    r = start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )
    return r.strftime("%Y%m%d")

ymd = random_date(datetime.datetime.strptime("2002-01-01", "%Y-%m-%d"), datetime.datetime.strptime("2024-01-01", "%Y-%m-%d"))
input_path = f"/vsicurl/https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/MUR-JPL-L4-GLOB-v4.1/{ymd}090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"
input_path = "/home/mdsumner/20240101090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"


## python cogger is not currently setting the offset/scale (for Celsius) 
dsn = f"vrt://NetCDF:\"{input_path}\":analysed_sst?a_offset=25&a_scale=0.001&a_srs=EPSG:4326"
ds = gdal.Open(dsn)
opts = gdal.WarpOptions(format = "COG", outputType = ds.GetRasterBand(1).DataType, 
     creationOptions = ["COMPRESS=ZSTD", "NUM_THREADS=ALL_CPUS", "PREDICTOR=2", "BLOCKSIZE=1024"]) 

## need to flesh this out, not sure if we should keep any or some
ds.SetMetadata({})
ds.GetRasterBand(1).SetMetadata({})
cog_file = "warp_analysed_sst.tif"

import pathlib
pathlib.Path(cog_file).unlink(missing_ok=True)

gdal.Warp(cog_file, ds,  width = 36000, height = 18000,  outputBounds = [-180, 90, 180, -90], 
   resampleAlg = "bilinear", options = opts, multithread = True, warpMemoryLimit = 4096)
   
