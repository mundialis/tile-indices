FROM osgeo/grass-gis:current-alpine

# install python and pip3 and gzip
RUN apk add python3 py3-pip gzip

# federal state specific required apk installations, to be replaced within workflow yaml by setting alpine_packages

# python3 + pip3
ENV PATH="/opt/venv/bin:$PATH"
RUN /usr/bin/python3 -m venv --system-site-packages /opt/venv

# federal state specific required pip installations, to be replaced within workflow yaml by setting python_libs

# copy scripts
COPY . /src/tile-indices

WORKDIR /src/tile-indices

# federal state specific python/bash script, to be replaced within workflow yaml

# Test: Unzip tindex and check with ogrinfo
ARG TINDEX_PATH
RUN set -e; \
    gunzip -c "${TINDEX_PATH}" > /tmp/tindex_test.gpkg; \
    ogrinfo -so -al /tmp/tindex_test.gpkg | tee /tmp/ogrinfo.txt; \
    grep -Eq "Feature Count: [1-9]" /tmp/ogrinfo.txt; \
    rm -f /tmp/tindex_test.gpkg /tmp/ogrinfo.txt
