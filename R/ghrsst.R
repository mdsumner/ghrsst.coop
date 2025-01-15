ghrsst_dates <- function() {
  seq(as.Date("2002-06-01"), Sys.Date()-1, by = "1 day")
}

ghrsst_folder <- function(date) {
  format(date-1, "%Y/%m/%d")
}
ghrsst_filedate <- function(date) {
  format(date, "%Y%m%d")
}
ghrsst_baseurl <- function() {
  "https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/MUR-JPL-L4-GLOB-v4.1"
}
ghrsst_file <- function(date) {
  ymd <- ghrsst_filedate(date)
  sprintf("%s090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc", ymd)
}
ghrsst_url <- function(date) {
  sprintf("%s/%s", ghrsst_baseurl(), ghrsst_file(date))
}

ghrsst_virtual <- function(date) {
  sprintf("%s/%s/%s", ghrsst_baseurl(), ghrsst_folder(date), ghrsst_file(date))
}

ghrsst_extent <- function() {
  c(-179.995,180.0050,-89.995,89.995)
}

ghrsst_vsi <- function(date, sds = "analysed_sst") {
  input_path <- ghrsst_url(date)
  sprintf("vrt://NetCDF:\"/vsicurl/%s\":analysed_sst?a_ullr=-179.995,89.995,180.0050,-89.995&a_offset=25&a_scale=0.001&a_srs=EPSG:4326",
          input_path)
}

ghrsst_key <- function(date, sds, bucket) {
  file <- gsub("nc$", "tif", sprintf("%s_%s", ghrsst_file(date), sds))
  file.path("/vsis3", bucket)
}
