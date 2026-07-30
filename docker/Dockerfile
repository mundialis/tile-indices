FROM osgeo/grass-gis:current-alpine

# install python and pip3 and gzip
RUN apk add python3 py3-pip gzip

# federal state specific required apk installations, to be replaced within workflow yaml by setting alpine_packages

# python3 + pip3
ENV PATH="/opt/venv/bin:$PATH"
RUN /usr/bin/python3 -m venv --system-site-packages /opt/venv

RUN pip3 install remotezip

# copy scripts
COPY . /src/tile-indices

WORKDIR /src/tile-indices

RUN grass -c epsg:25832 /grassdb/HE_DTM --exec python3 DTM/HE/HE_DTM_tindex.py
