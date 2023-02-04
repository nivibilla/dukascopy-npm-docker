# dukascopy-npm-docker
 
## Building and running for the first time
run `docker build -t dukascopy_data_download .`
run `docker run -it --name dukascopy_daily dukascopy_data_download`

## Running afterwards and daily
run `docker start dukascopy_daily`

## Copy Data Out
run `docker cp dukascopy_daily:/dukascopy/download <insert_new_path_here>`