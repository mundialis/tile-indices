#!/bin/sh

############################################################################
#
# MODULE:       fetch_BB_DOM_list.sh
# AUTHOR(S):    Markus Neteler, Veronica Koess
# PURPOSE:      Fetch list of Brandenburg, Germany DOM files from
#               https://data.geobasis-bb.de/geobasis/daten/bdom/
# SPDX-FileCopyrightText: (c) 2023 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
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
