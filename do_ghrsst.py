# year = '2002'
# month = '06'
# day = '01'
# 
# jday = '152'  ## or '001'  '010' etc

## logic for the a_ullr below
#f <- "/rdsi/PUBLIC/raad/data/podaac-opendap.jpl.nasa.gov/opendap/allData/ghrsst/data/GDS2/L4/GLOB/JPL/MUR/v4.1/2002/152/20020601090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"
#lon <- rawdata(f, "lon")
#lat  <- rawdata(f, "lat")
#range(lat)
##[1] -89.99  89.99
#la <- seq(-89.99 - 0.001/2, 89.99 + 0.001/2, length.out = 17999)
#range(la)
##[1] -89.9905  89.9905
#range(diff(la))
##[1] 0.01000006 0.01000006
# length(la)
##[1] 17999
# range(diff(lat))
##[1] 0.009994507 0.010002136


from datetime import datetime
from os import path
#import rasterio
from osgeo import gdal
from osgeo import gdalconst
gdal.UseExceptions()
def do_ghrsst(datestring, subdatasets = ["analysed_sst"])
    #datetime.date(int('2002'), int('09'), int('05'))
    datestring = '2002-06-01'
    #datetime.strptime(datestring, '%Y-%m-%d')
    dt    = datetime.strptime(datestring, '%Y-%m-%d')
    year  = datetime.strftime(dt, "%Y")
    month = datetime.strftime(dt, "%m")
    day   = datetime.strftime(dt, "%d")
    jday  = datetime.strftime(dt, "%j")
    ## as at 
    filename = f'/rdsi/PUBLIC/raad/data/podaac-opendap.jpl.nasa.gov/opendap/allData/ghrsst/data/GDS2/L4/GLOB/JPL/MUR/v4.1/{year}/{jday}/{year}{month}{day}090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc'
    
    #gdal.TranslateOptions(options=None, format=None, outputType=0, bandList=None, maskBand=None, width=0, height=0, widthPct=0.0, heightPct=0.0, xRes=0.0, yRes=0.0, creationOptions=None, srcWin=None, projWin=None, projWinSRS=None, strict=False, unscale=False, scaleParams=None, exponents=None, outputBounds=None, outputGeotransform=None, metadataOptions=None, outputSRS=None, nogcp=False, GCPs=None, noData=None, rgbExpand=None, stats=False, rat=True, xmp=True, resampleAlg=None, overviewLevel='AUTO', callback=None, callback_data=None)
    opts = gdal.TranslateOptions(format = "COG", outputType = gdalconst.GDT_Int16, 
     creationOptions = [ "BLOCKSIZE=1024",  "COMPRESS=ZSTD", "PREDICTOR=STANDARD", "RESAMPLING=AVERAGE", "SPARSE_OK=YES"])
    if path.isfile(filename): 
        ## loop over sds
        for sds in subdatasets: 
            ## FIXME:
            ##   rather than if/else hack there's a thing where you set up cases to do for?
            ##   we need to also drop the band metatadata about being in Kelvin
            if sds == "analysed_sst" | sds == "analysis_error":
                dsn = f"vrt://NetCDF:\"{filename}\":{sds}?a_srs=OGC:CRS84&a_ullr=-180,89.9905,180,-89.9905&a_scale=0.001&a_offset=25"
            else: 
                dsn = f"vrt://NetCDF:\"{filename}\":{sds}?a_srs=OGC:CRS84&a_ullr=-180,89.9905,180,-89.9905"
            ds = gdal.Open(dsn)
            ## can't use regex how do I bind it to end of string?
            #destName = filename.replace(".nc", f"{sds}.tif")
            destName = path.join("/tmp", path. file.nc.replace(".nc", f"{sds}.tif")
            ## remember ice, sst, mask, error have different types and offset/scale so a_scale/a_offset needs to be a special case
            ## and also you must update the band metadata tags which include offset/scale
            gdal.Translate('/tmp/somenw_deflate.tif', ds, format = "COG", outputType = ds.GetRasterBand(1).DataType, options = opts)



# new_dataset = rasterio.open(
#     '/tmp/new.tif',
#     'w',
#     driver='COG',
#     height= 1024, #$ds.shape[0],
#     width= 1024, #ds.shape[1],
#     count=1,
#     dtype=ds.dtypes[0],
#     crs=ds.crs,
#     transform=ds.transform, blocksize = 1024, compress = "zstd", predictors = "standard", resampling = "average"
# )

