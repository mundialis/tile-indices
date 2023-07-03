FROM osgeo/grass-gis:stable-alpine

# installations for DOP NW tindex
RUN apk add lynx parallel

# installations for ALKIS LK HE tindex
RUN pip3 install requests remotezip

# copy scripts
COPY . /src/tile-indices

WORKDIR /src/tile-indices

RUN grass -c epsg:25832 /grassdb/HE_ALKIS --exec python3 ALKIS/Liegenschaftskataster/HE/HE_ALKIS_LK_tindex.py
