This folder contains a tileindex for DSM tiles (in this case bDOM with size of 1000 x 1000 m) of Hamburg. It was created by using a python script.

Tile index:
- `hh_dom_tindex_proj.gpkg.gz`
- contains one poylgon for every tile
- filenames of the [ZIP](https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitales_hoehenmodell_bdom/DOM1_XYZ_HH_2020_04_30.zip)
  for each poylgon is stored as attribute ("location")

Download script:
- `HH_DSM_tindex.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents

Metadata:
- data can be used citing the „Freie und Hansestadt Hamburg, Landesbetrieb Geoinformation und Vermessung (LGV), [Datenlizenz Deutschland - Namensnennung - Version 2.0](https://www.govdata.de/dl-de/by-2-0), [bDOM](https://metaver.de/trefferanzeige?docuuid=2AB332A1-B1B6-4706-9546-33F0B1EADB6D)“

Links:
- [metadata, license, ...](https://metaver.de/trefferanzeige?docuuid=2AB332A1-B1B6-4706-9546-33F0B1EADB6D)
- [direct download](https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitales_hoehenmodell_bdom/DOM1_XYZ_HH_2020_04_30.zip)