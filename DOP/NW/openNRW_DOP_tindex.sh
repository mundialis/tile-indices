#!/bin/bash

############################################################################
#
# NAME:         openNRW_DOP_tindex.sh
#
# AUTHOR(S):    Markus Neteler <neteler at mundialis.de>
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Create tile index of openNRW DOP 10cm imagery files
#               - created from https://github.com/mundialis/openNRW/blob/master/dop/01_fetch_openNRW_DOP_list.sh
#
# Data source:  https://www.opengeodata.nrw.de/produkte/geobasis/dop/dop/
#
# COPYRIGHT:    (C) 2018-2023 by Markus Neteler, Anika Weinmann, mundialis
#
# REQUIREMENTS: lynx, gdal, gzip, sed
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
############################################################################

# Usage:
#   bash openNRW_DOP_tindex.sh
# Output:
#   NW_DOP10_tileindex.gpkg.gz
#
######
# fail early
# set -x

# set parallel processes
PJOBS=4
NUM_DOPS=10000

########################################
cd DOP/NW/

# Digitale Orthophotos (10-fache Kompression) - Paketierung: Einzelkacheln
URL=https://www.opengeodata.nrw.de/produkte/geobasis/lusat/dop/dop_jp2_f10/

#### check if we have lynx tool
if [ ! -x "`which lynx`" ] ; then
    echo "lynx required, please install lynx first"
    exit 1
fi

# gdalinfo /vsicurl/https://www.opengeodata.nrw.de/produkte/geobasis/lusat/dop/dop_jp2_f10/dop10rgbi_32_531_5744_1_nw_2022.jp2 # > test.txt

# ## test case: a few DOPs only
# echo "/vsicurl/https://www.opengeodata.nrw.de/produkte/geobasis/lusat/dop/dop_jp2_f10/dop10rgbi_32_531_5744_1_nw_2022.jp2" > opengeodata_nrw_dop10_URLs.csv
# echo "/vsicurl/https://www.opengeodata.nrw.de/produkte/geobasis/lusat/dop/dop_jp2_f10/dop10rgbi_32_531_5745_1_nw_2022.jp2" >> opengeodata_nrw_dop10_URLs.csv

# full tile index with 35860 NRW DOPs
lynx -dump -nonumbers -listonly $URL | grep www.opengeodata.nrw.de/produkte/geobasis/lusat/dop/ | grep 'jp2$' | sed 's+^+/vsicurl/+g' > opengeodata_nrw_dop10_URLs.csv

# divide csv file in more files
mkdir -p tmp_dop_nw_tindices
NUM=0
FILE_NUM=0
while read -r line
do
  ((NUM++))
  if [[ ${NUM} -le ${NUM_DOPS} ]]
  then
    ((FILE_NUM++))
    NUM=0
  fi
  FILE_NAME="tmp_dop_nw_tindices/tindex_${FILE_NUM}.csv"
  echo $line >> ${FILE_NAME}
done <opengeodata_nrw_dop10_URLs.csv

# create tindices
for CSV_FILE in $(ls tmp_dop_nw_tindices/*.csv) ; do
  echo "Tindex for $CSV_FILE ..."
  sem -j$PJOBS "gdaltindex -f GPKG ${CSV_FILE/csv/gpkg} --optfile ${CSV_FILE}"
done
sem --wait

# merge tindices to one tindex
for GPKG_FILE in $(ls tmp_dop_nw_tindices/*.gpkg)
do
  echo $GPKG_FILE
  ogr2ogr -f gpkg -update -append -unsetFid -nln openNRW_DOP10_tileindex openNRW_DOP10_tileindex.gpkg ${GPKG_FILE}
done

# verify
echo "Verifying vector tile index:"
ogrinfo -so -al openNRW_DOP10_tileindex.gpkg
# package
rm -f openNRW_DOP10_tileindex.gpkg.gz
gzip openNRW_DOP10_tileindex.gpkg
echo "<openNRW_DOP10_tileindex.gpkg.gz> created"

# cleanup
rm opengeodata_nrw_dop10_URLs.csv
rm -rf tmp_dop_nw_tindices
