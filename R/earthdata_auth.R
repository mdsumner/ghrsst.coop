file_earthdata <- function() {
  Sys.getenv("GDAL_HTTP_HEADER_FILE")
}

env_earthdata <- function() {
  Sys.getenv("GDAL_HTTP_HEADERS")
}
## check for env setting for earthdata (and include a test)
file_earthdata_auth <- function() {
  file <- file_earthdata()
  nzchar(file) && file.exists(file)
}
env_earthdata_auth <- function() {
  header <- env_earthdata()
    nzchar(header)
}


has_earthdata_auth <- function() {
    file_earthdata_auth() || env_earthdata_auth()
}


curl_auth_code <- function() {
  print(
  '
  authorization <- Sys.getenv("GDAL_HTTP_HEADERS")
  h <- curl::new_handle()
  curl::handle_setopt(h,  customrequest = "GET")
  curl::handle_setheaders(h, "Authorization" = gsub("Authorization: ", "", authorization))
  curl::curl_download(file.path(base, file), tf, handle = h)
  '
  )
  invisible(NULL)
}
