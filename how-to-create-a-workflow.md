# How to create a new workflow for a tile index

For each federal state there is a `./.github/workflow/tindices_<FS>.yml` (e.g. [tindices_nw.yml](./.github/workflows/tindices_nw.yml)). In this file the jobs for each tile index are defined by using the [tindex_creation](./.github/workflows/tindex_creation.yml) workflow. E.g. by

```yaml
  # DOP
  update-tindex-dop-sn:
    uses: ./.github/workflows/tindex_creation.yml
    with:
      type: DOP
      state: SN
      script: DOP_tileindex_SN.py
      tindex_file: DOP20_tileindex_SN.gpkg.gz
      alpine_packages: "firefox"
      python_libs: "selenium"

```

The following parameters must be set:

* `type`: The type of the tindex which must match the folder name, e.g. _DOP_, _DTM_, _DSM_, _nDSM_, _iDSM_
* `state`: The federal state abbreviation, e.g. _SN_
* `script`: The name of the python script for the creation of the tile index, e.g. _DOP_tileindex_SN.py_
* `tindex_file`: The name of the created tile index, e.g. _DOP20_tileindex_SN.gpkg.gz_

Optinal parameters are:

* `alpine_packages`: A list with alpine packages which need to be installed for tile index creation (seperated by space); e.g. _"firefox lynx"_
* `python_libs`: : A list with python libraries which need to be installed for tile index creation (seperated by space); e.g."selenium pandas"
* `epsg_for_grass`: The number of the EPSG code if GRASS GIS has to be used to run the python script; e.g. _25832_ or _25833_

If a new federal state is added, the workflow has to be added in the [main.yml](./.github/workflows/main.yml).