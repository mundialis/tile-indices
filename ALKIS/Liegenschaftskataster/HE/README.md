# Hessen ALKIS Liegenschaftskataster tile index

The tile index for teh Hessen ALKIS Liegenschaftskataster can be created with
[this script](HE_ALKIS_LK.py).

It creates the tile index [HE_ALKIS_LK_tindex.gpkg](HE_ALKIS_LK_tindex.gpkg)
with the column `location` which has as entry the url of the zip files for each
community of Hessen. The url has the placeholder `DATE` inside where the
current date has to be set with the format `YYYYMMDD`.
