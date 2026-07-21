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

URL = ("https://geodaten.schleswig-holstein.de/gaialight-sh/_apps/dladownload/single.php?file=bDOM_SH_Massendownload.geojson&id=4")
OUTPUT_FILE = []
os.chdir("iDSM/SH/")

# get GeoJson from URL
tmp_geojson = "/tmp/bDOM_SH__Massendownload.geojson"
os.system(f'curl -L "{URL}" -o "{tmp_geojson}"')

# create GPKG from GeoJson
tindex_gpkg = "sh_bdom_tindex_proj.gpkg"
stream = os.popen(f"ogr2ogr {tindex_gpkg} {tmp_geojson}")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen(f"ogrinfo -so -al {tindex_gpkg}")
tindex_verification = stream.read()
print(tindex_verification)

# package
OUTPUT_FILE = (f"{tindex_gpkg}.gz")
if os.path.isfile(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)
stream = os.popen(f"gzip {tindex_gpkg}")
create_gz = stream.read()
print(f"<{OUTPUT_FILE}> created")

# cleanup
if os.path.isfile(tindex_gpkg):
    os.remove(tindex_gpkg)
if os.path.isfile(tmp_geojson):
    os.remove(tmp_geojson)
