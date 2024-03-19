#export PYTHONPATH=:/usr/local/lib/python3/dist-packages
#export RETICULATE_PYTHON=/usr/bin/python3
#export GDAL_HTTP_HEADER_FILE=/home/mdsumner/earthdata

import odc
import os
import xarray as xr
from odc.geo.geobox import GeoBox
from odc.geo.xr import assign_crs, xr_reproject
from odc.geo.cog import write_cog
import affine
import pathlib
from pathlib import Path
import fsspec
headers = {"Authorization": f"Bearer {os.environ['EARTHDATA_TOKEN']}"}

VARIABLES = [
    "analysed_sst",
    "analysis_error",
    "mask",
    "sea_ice_fraction",
    "sst_anomaly",
    "dt_1km_data",
]

DROP_VARIABLES = ["dt_1km_data",     "analysis_error",
    "mask",
    "sea_ice_fraction",
    "sst_anomaly"]
VARIABLES = [var for var in VARIABLES if var not in DROP_VARIABLES]

## write_cog is not respecting blocksize
COG_OPTS = dict(COMPRESS = "ZSTD", NUM_THREADS = "ALL_CPUS", BLOCKSIZE = "1024")

import datetime
import random


def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    r = start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )
    return r.strftime("%Y%m%d")

ymd = random_date(datetime.datetime.strptime("2002-01-01", "%Y-%m-%d"), datetime.datetime.strptime("2024-01-01", "%Y-%m-%d"))


input_path = f"https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/MUR-JPL-L4-GLOB-v4.1/{ymd}090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"


with fsspec.open(input_path, headers=headers) as f:
                data = xr.open_dataset(
                    f,
                    mask_and_scale=False,
                    drop_variables=DROP_VARIABLES,
                    engine="h5netcdf",
                ).load()
  

data = assign_crs(data, crs="EPSG:4326")
 
                
new_geobox = GeoBox(
        data.odc.geobox.shape,
        affine.Affine(0.01, 0.0, -180.0, 0.0, 0.01, -89.995),
        data.odc.geobox.crs,
    )
    

output_location = ""
var = "analysed_sst"
cog_file = f"odc_{var}.tif"


pathlib.Path(cog_file).unlink(missing_ok=True)


write_cog(data[var], cog_file, **COG_OPTS)


