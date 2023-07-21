#!/bin/sh

############################################################################
#
# NAME:        fetch_BB_DOM_list.sh
#
# AUTHOR(S):    Markus Neteler <neteler at mundialis.de>
#               Veronica Koess <koess at mundialis.de>
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Fetch list of Brandenburg, Germany DOM files
#
# Data source:  https://data.geobasis-bb.de/geobasis/daten/bdom/
#
# COPYRIGHT:    (C) 2023 by Markus Neteler, mundialis
#
# REQUIREMENTS: lynx, gdal, gTILE, sed
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
#   sh fetch_BB_DOM_list.sh
# Output:
#   BB_DOM_tiles.csv
########################################

lynx -dump -nonumbers -listonly https://data.geobasis-bb.de/geobasis/daten/bdom/tif/ | grep https://data.geobasis-bb.de/geobasis/daten/bdom/tif/bdom_| sed 's+^+/vsizip/vsicurl/+g' > BB_DOM_tiles.csv

# generate download script
# cat BB_DOM_tiles.csv | sed 's+^+wget -c +g' > fetch_bb_dom_urls.sh

# compress ndom50 URLs list
gzip BB_DOM_tiles.csv
echo "Generated <BB_DOM_tiles.csv.gz>"


echo "Single tile import: Import into GRASS GIS with, e.g.:
r.import input=/vsizip/vsicurl/https://data.geobasis-bb.de/geobasis/daten/bdom/xyz/bdom_33250-5890.zip/bdom_33250-5890.xyz output=bb_bdom_33250-5890"
echo ""
echo "For mosaics, better generate a VRT mosaic first (using <gdalbuildvrt ...>), then import the VRT file."
echo ""
echo "For a tile index, run
gdaltindex -f GPKG BB_DOM_tileindex.gpkg --optfile BB_DOM_tiles.csv"
