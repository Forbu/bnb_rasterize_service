### Web server for the BNB database

### Where to find and put the data

bnb export in gpkg : https://www.data.gouv.fr/en/datasets/base-de-donnees-nationale-des-batiments-version-0-6/

You have to put this in data/ repo.


For the json data (where are the region) : https://www.data.gouv.fr/en/datasets/contours-geographiques-des-nouvelles-regions-metropole/


### docker commands to launch

to build the docker images, simply tape :

docker build -t adrien/bnb .

to launch in bash mode :

docker run -it -v $PWD:/home/src/ -v /media/adrienb/BigOne/data/bnb_rasterize/gpkg/:/home/data/ adrien/bnb bash