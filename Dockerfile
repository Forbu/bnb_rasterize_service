FROM osgeo/gdal

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

# install geocube
RUN apt update -y 
RUN apt install -y git
RUN pip install geocube

# we install rasterio fiona 
RUN pip3 install rasterio fiona

# install numpy and matplotlib
RUN pip3 install numpy matplotlib

# install geopandas
RUN pip3 install geopandas

