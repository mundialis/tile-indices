FROM mundialis/grass-py3-pdal:releasebranch_8_2-ubuntu as grass
# FROM osgeo/grass-gis:stable-ubuntu as grass

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends --no-install-suggests \
    lynx parallel
COPY . /src/tile-indices

WORKDIR /src/tile-indices

RUN python3 DOP/NW/openNRW_DOP_tindex.py
