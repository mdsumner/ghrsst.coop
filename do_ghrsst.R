library(raadtools)
nmax <- 100
files <- ghrsstfiles()
st <- Sys.time()

# "/rdsi/PUBLIC/raad/data/podaac-opendap.jpl.nasa.gov/opendap/allData/ghrsst/data/GDS2/L4/GLOB/JPL/MUR/v4.1/2002/152/20020601090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"
# files$fullname[1]
outpath <- function(x, date) {
  # x <- gsub("podaac-opendap.jpl.nasa.gov/opendap/allData/ghrsst/data/GDS2/L4/GLOB/JPL/MUR/v4.1",
  #      "idea.public/ghrsst", x)
  #day <- format(date, "%j")
  year <- format(date, "%Y")
  file.path("/rdsi/PUBLIC/raad2/data/idea.public/ghrsst", year, gsub("\\.nc$", ".tif", basename(x)))
}

#all(stringr::str_detect(files$fullname, "podaac-opendap.jpl.nasa.gov/opendap/allData/ghrsst/data/GDS2/L4/GLOB/JPL/MUR/v4.1"))
#outpath(files$fullname[1])
dsnit <- function(x) {
  dsn <- dsn::vrtcon(dsn::sds(x, "analysed_sst", "netCDF"),
                     a_scale=0.001, a_offset = 25,
                     a_ullr="-180,90,180,-90", a_srs="OGC:CRS84")
  dsn
}
warpit <-
purrr::safely(
  function(x, out_dsn) {
   if (!dir.exists(dirname(out_dsn))) {
     dir.create(dirname(out_dsn), recursive = TRUE)
   }
  vapour::gdal_raster_dsn(x,  out_dsn = out_dsn,
                          target_dim = c(36000, 18000),
                          target_ext = c(-180, 180, -90, 90),
                          options=c("-nomd", "-overwrite",
                                    "-co", "COMPRESS=DEFLATE",
                                    "-of", "COG",
                                    "-co", "BLOCKSIZE=1024",
                                    #"-co", "NUM_THREADS=4",
                                    "-co", "PREDICTOR=STANDARD",
                                    "-co", "RESAMPLING=AVERAGE",
                                    "-co", "SPARSE_OK=YES" #, "-multi"
))

}
)

files <- files[nrow(files):1, ]
files$out_dsn <- outpath(files$fullname, files$date)
files <- files[!fs::file_exists(files$out_dsn), ]

if (nrow(files) > nmax) {
  files <- files[seq_len(nmax), ]
}

library(furrr)
plan(multicore, workers = 18)
dofun <- function(.x) {
  dsn <- dsnit(.x$fullname)
  l <- warpit(dsn, .x$out_dsn)
  invisible(NULL)
}

future_map(split(files, 1:nrow(files)), dofun)

plan(sequential)


print("start time:")
print(st)

print(Sys.time())

