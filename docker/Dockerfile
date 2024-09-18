FROM osgeo/grass-gis:current-alpine

# installations for DOP NW tindex
RUN apk add lynx parallel

# install firefox and xsel for DOP SN tindex
RUN apk add firefox xsel

# installations for ALKIS LK HE tindex
RUN pip3 install requests remotezip

# copy scripts
COPY . /src/tile-indices

WORKDIR /src/tile-indices

# overwrite the script in workflow yaml to create other tindices
RUN python3 DOP/NW/openNRW_DOP_tindex.py
