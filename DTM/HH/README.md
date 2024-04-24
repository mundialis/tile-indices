This folder contains a tileindex for DTM tiles (in this case DGM1 with size of 2000 x 2000 m) of Hamburg. It was created by using a python script.

Tile index:
- `hh_dgm1_tindex_proj.gpkg.gz`
- contains one poylgon for every tile
- filenames (of the [ZIP](https://daten-hamburg.de/geographie_geologie_geobasisdaten/Digitales_Hoehenmodell/DGM1/dgm1_2x2km_XYZ_hh_2021_04_01.zip))
for each poylgon is stored as attribute ("location")

Download script:
- `HH_DTM_tindex.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents

Metadata:
- data can be used citing the „Freie und Hansestadt Hamburg, Landesbetrieb Geoinformation und Vermessung (LGV), [Datenlizenz Deutschland - Namensnennung - Version 2.0](https://www.govdata.de/dl-de/by-2-0), [DGM1](https://metaver.de/trefferanzeige?docuuid=A39B4E86-15E2-4BF7-BA82-66F9913D5640)“

Links:
- [metadata, license, ...](https://metaver.de/trefferanzeige?docuuid=A39B4E86-15E2-4BF7-BA82-66F9913D5640)
- [direct download](https://daten-hamburg.de/geographie_geologie_geobasisdaten/Digitales_Hoehenmodell/DGM1/dgm1_2x2km_XYZ_hh_2021_04_01.zip)