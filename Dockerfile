FROM osgeo/gdal

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    libgeos++-dev \
    && rm -rf /var/lib/apt/lists/*

# COPY whole package and then install it with pip
WORKDIR /home
#COPY . .
#RUN pip3 install .

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

# install pytest
RUN pip3 install pytest
RUN pip3 install geoplot

# install flask
RUN pip3 install flask

# create directories
RUN mkdir /home/data/
RUN mkdir /home/src/

# port mapping between 5000 in the container and 5000 on the host for the flask app
EXPOSE 5000
