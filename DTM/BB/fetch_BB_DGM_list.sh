#!/bin/sh

############################################################################
#
# MODULE:       fetch_BB_DGM_list.sh
# AUTHOR(S):    Markus Neteler, Veronica Koess
# PURPOSE:      Fetch list of Brandenburg, Germany DGM from
#               https://data.geobasis-bb.de/geobasis/daten/dgm/
# SPDX-FileCopyrightText: (c) 2020 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
############################################################################

# Usage:
#   sh fetch_BB_DGM.sh
# Output:
#   BB_DGM_tiles.csv
########################################

lynx -dump -nonumbers -listonly https://data.geobasis-bb.de/geobasis/daten/dgm/xyz/ | grep https://data.geobasis-bb.de/geobasis/daten/dgm/xyz/dgm | sed 's+^+/vsizip/vsicurl/+g' > BB_DGM_tiles.csv

# generate download script
# cat BB_DGM_tiles.csv | sed 's+^+wget -c +g' > fetch_bb_dom_urls.sh

# compress ndom50 URLs list
gzip BB_DGM_tiles.csv
echo "Generated <BB_DGM_tiles.csv.gz>"


echo "Single tile import: Import into GRASS GIS with, e.g.:
r.import input=/vsizip/vsicurl/https://data.geobasis-bb.de/geobasis/daten/dgm/xyz/dgm_33255-5889.zip/dgm_33255-5889.xyz output=dgm_33255-5889"
echo ""
echo "For mosaics, better generate a VRT mosaic first (using <gdalbuildvrt ...>), then import the VRT file."
echo ""
echo "For a tile index, run
gdaltindex -f GPKG BB_DGM_tileindex.gpkg --optfile BB_DGM_tiles.csv"
