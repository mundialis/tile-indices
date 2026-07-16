############################################################################
#
# MODULE:      SH_idsm_tindex
# AUTHOR(S):   Kim Kaiser
# PURPOSE:     Creates a tile index of Schleswig-Holstein iDSM files
# SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
#############################################################################

import os
import json

URL = ("https://github.com/kimariak/tile-indices/blob/main/iDSM/SH/bDOM_SH_tindex.geojson")
OUTPUT_FILE = "sh_bdom_tindex_proj.gpkg.gz"
os.chdir("iDSM/SH/")

# create GPKG from GeoJson
tindex_gpkg = OUTPUT_FILE.rsplit(".", 1)[0]
stream = os.popen(f"ogr2ogr {tindex_gpkg} {URL}")
stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen(f"ogrinfo -so -al {tindex_gpkg}")
tindex_verification = stream.read()
print(tindex_verification)

# package
if os.path.isfile(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)
stream = os.popen(f"gzip {tindex_gpkg}")
stream.read()
print(f"<{OUTPUT_FILE}> created")

# cleanup
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile(tindex_gpkg):
    os.remove(tindex_gpkg)
