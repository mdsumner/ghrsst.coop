

## COPY
#s3path <- file.path("s3://idea-ghrsst", ymdpath) #, gsub(".nc$", "_analysed_sst.tif", file))
#gsub("/vsimem", "/vsis3/idea-ghrsst", output_path)


#gdalraster::translate(dsn, output_path, cl_arg = gdal_options)

#cmd <- sprintf("rclone copy %s %s", output_path, s3path)
#system(cmd)

# con <- new(VSIFile, output_path, "r")
# bytes <- con$ingest(-1)
#  con$close()

#print(s3path)
#return(bytes)

# con <- new(VSIFile, s3path, "w")
# con$write(bytes)
# con$close()
#cmd <- sprintf("gdal_translate  '%s' %s %s", dsn, output_path, paste0(gdal_options, collapse = " "))
#system(cmd)
