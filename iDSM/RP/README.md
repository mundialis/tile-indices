This folder contains a tileindex for iDSM tiles (in this case iDSM20 with size of 2000 x 2000 m) of Rheinland-Pfalz. It was created by using a python script.

Tile index:
- `rp_idsm_tindex_proj.gpkg.gz`
- contains one poylgon for every tile
- download links of the LAS data are stored as attribute "location"

Download script:
- `RP_iDSM_tindex.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents

Metadata:
- data can be used by citing "©GeoBasis-DE / LVermGeoRP", [Datenlizenz Deutschland Namensnennung 2.0](https://www.govdata.de/dl-de/by-2-0), [Geoportal RLP](www.lvermgeo.rlp.de)"

Links:
- [metadata, license, ...](https://www.geoportal.rlp.de/mapbender/php/mod_iso19139ToHtml.php?url=https%3A%2F%2Fwww.geoportal.rlp.de%2Fmapbender%2Fphp%2Fmod_dataISOMetadata.php%3FoutputFormat%3Diso19139%26id%3D3d2dda7d-b4b5-47d2-b074-dd45edd36738)
