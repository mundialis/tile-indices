FROM mundialis/grass-py3-pdal:releasebranch_8_2-alpine as grass
# FROM osgeo/grass-gis:stable-alpine as grass

RUN apk add lynx

COPY . /src/tile-indices

WORKDIR /src/tile-indices

RUN sh DOP/NW/openNRW_DOP_tindex.sh
