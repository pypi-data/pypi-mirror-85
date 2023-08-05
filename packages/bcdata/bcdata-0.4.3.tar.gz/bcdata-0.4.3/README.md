# bcdata

Python and command line tools for quick access to DataBC geo-data available via WFS/WCS.

[![Build Status](https://travis-ci.org/smnorris/bcdata.svg?branch=master)](https://travis-ci.org/smnorris/bcdata)
[![Coverage Status](https://coveralls.io/repos/github/smnorris/bcdata/badge.svg?branch=master)](https://coveralls.io/github/smnorris/bcdata?branch=master)

There is a [wealth of British Columbia geographic information available as open
data](https://catalogue.data.gov.bc.ca/dataset?download_audience=Public),
but direct file download urls are not available and the syntax to accesss WFS via `ogr2ogr` and/or `curl/wget` can be awkward.

This Python module and CLI attempts to simplify downloads of BC geographic data and smoothly integrate with existing Python GIS tools like `geopandas`, `fiona` and `rasterio`.


## Disclaimer

- it is the user's responsibility to check the licensing for any downloads, data are generally licensed as [OGL-BC](http://www2.gov.bc.ca/gov/content/governments/about-the-bc-government/databc/open-data/open-government-license-bc)
- this is not specifically endorsed by the Province of Britsh Columbia or DataBC
- use with care, please don't overload the service


## Installation

    $ pip install bcdata

To enable autocomplete of dataset names (full object names only) with the command line tools, add this line to your `.bashrc` as per this [guide](https://click.palletsprojects.com/en/7.x/bashcomplete/?highlight=autocomplete#activation).

    eval "$(_BCDATA_COMPLETE=source bcdata)"

## Usage

Typical usage will involve a manual search of the [DataBC Catalogue](https://catalogue.data.gov.bc.ca/dataset?download_audience=Public) to find a layer of interest. Once a dataset of interest is found, note the key with which to retreive it. This can be either the `id`/`package name` (the last portion of the url) or the `Object Name` (Under `Object Description`).

For example, for [BC Airports]( https://catalogue.data.gov.bc.ca/dataset/bc-airports), either of these keys will work:

- id/package name: `bc-airports`
- object name: `WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW`

Note that some packages [may have more than one layer](https://catalogue.data.gov.bc.ca/dataset/forest-development-units) - if you request a package like this, `bcdata` will prompt you with a list of valid object/table names to use instead of the package name.

### Python module

```python
import bcdata

# get a feature as geojson
geojson = bcdata.get_data(
    'bc-airports',
    query="AIRPORT_NAME='Terrace (Northwest Regional) Airport'"
)
geojson
{'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': 'WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW.fid-f0cdbe4_16811fe142b_-6f34', 'geometry': {'type': 'Point', ...

# optionally, load data as a geopandas GeoDataFrame
gdf = bcdata.get_data(
    'bc-airports',
    query="AIRPORT_NAME='Terrace (Northwest Regional) Airport'",
    as_gdf=True
)
gdf.head()
AERODROME_STATUS AIRCRAFT_ACCESS_IND                          AIRPORT_NAME                ...                TC_LID_CODE WEBSITE_URL                          geometry
0        Certified                   Y  Terrace (Northwest Regional) Airport                ...                       None        None  POINT (-128.5783333 54.46861111)
```

### CLI

There are several commands available:

    $ bcdata --help
    Usage: bcdata [OPTIONS] COMMAND [ARGS]...

    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.

    Commands:
      bc2pg  Download a DataBC WFS layer to postgres - an ogr2ogr wrapper.
      cat    Write DataBC features to stdout as GeoJSON feature objects.
      dem    Dump BC DEM to TIFF
      dump   Write DataBC features to stdout as GeoJSON feature collection.
      info   Print basic metadata about a DataBC WFS layer as JSON.
      list   List DataBC layers available via WFS


#### `list`

    $ bcdata list --help
    Usage: bcdata list [OPTIONS]

      List DataBC layers available via WFS

    Options:
      -r, --refresh  Refresh the cached list
      --help         Show this message and exit.


#### `info`

    $ bcdata info --help
    Usage: bcdata info [OPTIONS] DATASET

      Print basic metadata about a DataBC WFS layer as JSON.

      Optionally print a single metadata item as a string.

    Options:
      --indent INTEGER  Indentation level for JSON output
      --count           Print the count of features.
      --name            Print the datasource's name.
      --help            Show this message and exit.


#### `dump`

    $ bcdata dump --help
    Usage: bcdata dump [OPTIONS] DATASET

      Write DataBC features to stdout as GeoJSON feature collection.

        $ bcdata dump bc-airports
        $ bcdata dump bc-airports --query "AIRPORT_NAME='Victoria Harbour (Shoal Point) Heliport'"
        $ bcdata dump bc-airports --bounds xmin ymin xmax ymax

       It can also be combined to read bounds of a feature dataset using Fiona:
         $ bcdata dump bc-airports --bounds $(fio info aoi.shp --bounds)

    Options:
      --query TEXT                    A valid CQL or ECQL query, quote enclosed (h
                                      ttps://docs.geoserver.org/stable/en/user/tut
                                      orials/cql/cql_tutorial.html)
      -o, --out_file TEXT             Output file
      --bounds TEXT                   Bounds: "left bottom right top" or "[left,
                                      bottom, right, top]". Coordinates are BC
                                      Albers (default) or --bounds_crs
      --bounds-crs, --bounds_crs TEXT
                                      CRS of provided bounds
      -v, --verbose                   Increase verbosity.
      -q, --quiet                     Decrease verbosity.
      --help                          Show this message and exit.

#### `cat`

    $ bcdata cat --help
    Usage: bcdata cat [OPTIONS] DATASET

      Write DataBC features to stdout as GeoJSON feature objects.

    Options:
      --query TEXT                    A valid `CQL` or `ECQL` query (https://docs.
                                      geoserver.org/stable/en/user/tutorials/cql/c
                                      ql_tutorial.html)
      --bounds TEXT                   Bounds: "left bottom right top" or "[left,
                                      bottom, right, top]". Coordinates are BC
                                      Albers (default) or --bounds_crs
      --indent INTEGER                Indentation level for JSON output
      --compact / --not-compact       Use compact separators (',', ':').
      --dst-crs, --dst_crs TEXT       Destination CRS.
      -p, --pagesize INTEGER          Max number of records to request
      -s, --sortby TEXT               Name of sort field
      --bounds-crs, --bounds_crs TEXT
                                      CRS of provided bounds
      -v, --verbose                   Increase verbosity.
      -q, --quiet                     Decrease verbosity.
      --help                          Show this message and exit.


#### `dem`

    $ bcdata dem --help
    Usage: bcdata dem [OPTIONS]

      Dump BC DEM to TIFF

    Options:
      -o, --out_file TEXT             Output file
      --bounds TEXT                   Bounds: "left bottom right top" or "[left,
                                      bottom, right, top]". Coordinates are BC
                                      Albers (default) or --bounds_crs  [required]
      --dst-crs, --dst_crs TEXT       Destination CRS.
      --bounds-crs, --bounds_crs TEXT
                                      CRS of provided bounds
      -r, --resolution INTEGER
      -v, --verbose                   Increase verbosity.
      -q, --quiet                     Decrease verbosity.
      --help                          Show this message and exit.


#### `bc2pg`

    $ bcdata bc2pg --help
    Usage: bcdata bc2pg [OPTIONS] DATASET

      Download a DataBC WFS layer to postgres - an ogr2ogr wrapper.

         $ bcdata bc2pg bc-airports --db_url postgresql://postgres:postgres@localhost:5432/postgis

      The default target database can be specified by setting the $DATABASE_URL
      environment variable.
      https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls

    Options:
      -db, --db_url TEXT              SQLAlchemy database url
      --table TEXT                    Destination table name
      --schema TEXT                   Destination schema name
      --query TEXT                    A valid `CQL` or `ECQL` query (https://docs.
                                      geoserver.org/stable/en/user/tutorials/cql/c
                                      ql_tutorial.html)
      --bounds TEXT                   Bounds: "left bottom right top" or "[left,
                                      bottom, right, top]". Coordinates are BC
                                      Albers (default) or --bounds_crs
      --bounds-crs, --bounds_crs TEXT
                                      CRS of provided bounds
      -p, --pagesize INTEGER          Max number of records to request
      -w, --max_workers INTEGER       Max number of concurrent requests
      --dim TEXT                      Force the coordinate dimension to val (valid
                                      values are XY, XYZ)
      --fid TEXT                      Primary key of dataset
      --append                        Append data to existing table
      -v, --verbose                   Increase verbosity.
      -q, --quiet                     Decrease verbosity.
      --help                          Show this message and exit.


#### CLI examples

Search the data listing for airports:

      $ bcdata list | grep AIRPORTS
      WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW

Describe a dataset. Note that if we know the id of a dataset, we can use that rather than the object name:

    $ bcdata info bc-airports --indent 2
    {
      "name": "WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW",
      "count": 455,
      "schema": {
        "properties": {
          "CUSTODIAN_ORG_DESCRIPTION": "string",
          "BUSINESS_CATEGORY_CLASS": "string",
          "BUSINESS_CATEGORY_DESCRIPTION": "string",
          "OCCUPANT_TYPE_DESCRIPTION": "string",
          ...etc...
        },
        "geometry": "GeometryCollection",
        "geometry_column": "SHAPE"
      }
    }

The JSON output can be manipulated with [jq](https://stedolan.github.io/jq/). For example, to show only the fields available in the dataset:

    $ bcdata info bc-airports | jq '.schema.properties'
    {
      "CUSTODIAN_ORG_DESCRIPTION": "string",
      "BUSINESS_CATEGORY_CLASS": "string",
      "BUSINESS_CATEGORY_DESCRIPTION": "string",
      "OCCUPANT_TYPE_DESCRIPTION": "string",
      etc...
    }

Dump data to geojson ([`EPSG:4326` only](https://tools.ietf.org/html/rfc7946#section-4)):

    $ bcdata dump bc-airports > bc-airports.geojson

Get a single feature and send it to geojsonio (requires [geojson-cli](https://github.com/mapbox/geojsonio-cli)).  Note the double quotes  required around a CQL FILTER provided to the `--query` option.

    $ bcdata dump \
      WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW \
      --query "AIRPORT_NAME='Terrace (Northwest Regional) Airport'" \
       | geojsonio

Save a layer to a geopackage in BC Albers:

    $ bcdata cat bc-airports --dst-crs EPSG:3005 \
      | fio collect \
      | fio load -f GPKG --dst-crs EPSG:3005 airports.gpkg

Load a couple of layer to postgres and run a query:

    $ bcdata bc2pg bc-airports \
        --db_url postgresql://postgres:postgres@localhost:5432/postgis

    $ bcdata bc2pg WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_MUNICIPALITIES_SP \
        --db_url postgresql://postgres:postgres@localhost:5432/postgis

    $ psql -c \
      "SELECT airport_name
       FROM whse_imagery_and_base_maps.gsr_airports_svw a
       INNER JOIN whse_legal_admin_boundaries.abms_municipalities_sp m
       ON ST_Intersects(a.geom, m.geom)
       WHERE admin_area_name LIKE '%Victoria%'"
                               airport_name
    ------------------------------------------------------------------
     Victoria Harbour (Camel Point) Heliport
     Victoria Inner Harbour AirportÂ (Victoria Harbour Water Airport)
     Victoria Harbour (Shoal Point) Heliport
    (3 rows)

Note that the `Â` shown in the harbour airport name is present in the source data, this is not a bcdata or encoding issue.


## Projections / CRS

**CLI**

`bcdata dump` returns GeoJSON in WGS84 (`EPSG:4326`).

`bcdata cat` provides the `--dst-crs` option, use any CRS the WFS server supports.

`bcdata bc2pg` loads data to PostgreSQL in BC Albers (`EPSG:3005`).


**Python module**

`bcdata.get_data()` defaults to `EPSG:4236` but any CRS can be specified (that the server will accept).


## Development and testing

    $ mkdir bcdata_env
    $ virtualenv bcdata_env
    $ source bcdata_env/bin/activate
    (bcdata_env)$ git clone git@github.com:smnorris/bcdata.git
    (bcdata_env)$ cd bcdata
    (bcdata_env)$ pip install -e .[test]
    (bcdata_env)$ py.test


## Other implementations
- [bcdata R package](https://github.com/bcgov/bcdata)
- [OWSLib](https://github.com/geopython/OWSLib) has basic WFS capabilities
- GDAL / curl / wget:

        # list all layers
        # querying the endpoint this way doesn't seem to work with `VERSION=2.0.0`
        ogrinfo WFS:http://openmaps.gov.bc.ca/geo/ows?VERSION=1.1.0

        # define a request url for airports
        airports_url="https://openmaps.gov.bc.ca/geo/pub/WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW&outputFormat=json&SRSNAME=epsg%3A3005"

        # describe airports
        ogrinfo -so $airports_url OGRGeoJSON

        # dump airports to geojson
        ogr2ogr \
          -f GeoJSON \
          airports.geojson \
          $airports_url

        # load airports to postgres
        ogr2ogr \
          -f PostgreSQL \
          PG:"host=localhost user=postgres dbname=postgis password=postgres" \
          -lco SCHEMA=whse_imagery_and_base_maps \
          -lco GEOMETRY_NAME=geom \
          -nln gsr_airports_svw \
          $airports_url

        # Try requesting a larger dataset - ungulate winter range
        uwr_url="https://openmaps.gov.bc.ca/geo/pub/WHSE_WILDLIFE_MANAGEMENT.WCP_UNGULATE_WINTER_RANGE_SP/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=WHSE_WILDLIFE_MANAGEMENT.WCP_UNGULATE_WINTER_RANGE_SP&outputFormat=json&SRSNAME=epsg%3A3005"

        # The request only returns the first 10,000 records
        ogr2ogr \
          uwr.shp \
          -dsco OGR_WFS_PAGING_ALLOWED=ON \
          $uwr_url

        # wget works too, but still only 10k records
        wget -O uwr.geojson $uwr_url
