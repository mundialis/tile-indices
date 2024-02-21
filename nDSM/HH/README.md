This folder contains a tileindex for nDSM tiles (in this case bDSM with size of 1000 x 1000 m) of Hamburg. It was created by using a python script.

Tile index:
- `nDSM_tileindex_HH.gpkg.gz`
- contains one poylgon for every tile
- filename for each poylgon is stored as attribute ("location")

Download script:
- `nDSM_tileindex_HH.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents
- requires the downloaded directory of bDSMs of Hamburg and its path (unzipped)
- requires an output file path (.gpkg)
- depending on the filename length the indexing in line 46 & 47 should be adjusted

Metadata:
- `metadata.json`
- data can be used citing the „Datenlizenz Deutschland - Namensnennung - Version 2.0“
- see file for complete metadata and license

Links:
- [metadata, license, ...](https://suche.transparenz.hamburg.de/dataset/digitales-hoehenmodell-hamburg-bdom4)
- [direct download](https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitales_hoehenmodell_bdom/DOM1_XYZ_HH_2020_04_30.zip)