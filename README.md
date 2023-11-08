
<!-- README.md is generated from README.Rmd. Please edit that file -->

# ghrsst.coop

<!-- badges: start -->
<!-- badges: end -->

The goal of ghrsst.coop is to convert GHRSST to cloud ready.

- **do_ghrsst.py** is in progress, does the job with osgeo.gdal GDAL API
- **do_ghrsst.R** is a record of first attempt, uses R package vapour
  with GDAL API, and has a few issues we’re improving on here

-\[ \] embed in logging framework and deploy -\[ \] fix band metadata to
reflect Celsius not Kelvin on the right bands -\[ \] clean up the python
-\[ \] compare to xarray/odc ways -\[ \] do all subdatasets

## Draft 1

See the R script do_ghrsst.R

See notes below.

## Draft 2

See the Python script do_ghrsst.py

See partner and more python-ic xarray/odc based project here:
<https://github.com/auspatious/ghrsst-cogger/>

### Draft 1 notes

We use the assign scale and offset trick to convert to Celsius without
changing the values from Int16.

We chose warper and to set to -180,180,-90,90 but in update we chose
what seems better aligned (there’s a half-row missing at the north and
south).

This commented R code shows the logic

``` r
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
```

## Code of Conduct

Please note that the ghrsst.coop project is released with a [Contributor
Code of
Conduct](https://contributor-covenant.org/version/2/1/CODE_OF_CONDUCT.html).
By contributing to this project, you agree to abide by its terms.
