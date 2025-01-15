typical_config <- function() {
  cat(
'#export GDAL_HTTP_HEADERS  for earthdata
#export AWS_ACCESS_KEY_ID= for write to Acacia
#export AWS_SECRET_ACCESS_KEY= ditto
#export AWS_S3_ENDPOINT=projects.pawsey.org.au #for resolving acacia
#export AWS_VIRTUAL_HOSTING=FALSE #to not use virtual bucket.host but host.bucket
#export CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE=YES  #to allow write via file for GEOTIFF
#export VSIS3_CHUNK_SIZE=50'
  )
  invisible(NULL)
}


gdal_options <- function() {
  c(
    "-co", "COMPRESS=ZSTD",
    "-of", "COG",
    "-co", "BLOCKSIZE=512",
    "-co", "PREDICTOR=STANDARD",
    "-co", "RESAMPLING=AVERAGE",
    "-co", "SPARSE_OK=YES", "-co",
    "NUM_THREADS=ALL_CPUS")
}
