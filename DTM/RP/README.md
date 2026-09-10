This folder contains a tileindex for DTM tiles (in this case DGM1 with size of 1000 x 1000 m) of Rheinland-Pfalz. It was created by using a python script.

Tile index:
- `rp_dtm_tindex_proj.gpkg.gz`
- contains one poylgon for every tile
- download links of the Tif data are stored as attribute "location"

Download script:
- `RP_DTM_tindex.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents

Metadata:
- data can be used by citing "©GeoBasis-DE / LVermGeoRP", [Datenlizenz Deutschland Namensnennung 2.0](https://www.govdata.de/dl-de/by-2-0), [Geoportal RLP](www.lvermgeo.rlp.de)"

Links:
- [metadata, license, ...](https://www.geoportal.rlp.de/mapbender/php/mod_iso19139ToHtml.php?url=https%3A%2F%2Fwww.geoportal.rlp.de%2Fmapbender%2Fphp%2Fmod_dataISOMetadata.php%3FoutputFormat%3Diso19139%26id%3Dab69aa3d-e786-41f8-95dc-7b34abb06c41#tabs-4)
