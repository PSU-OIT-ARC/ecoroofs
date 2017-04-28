# EcoRoofs

A web-mapping application for green roofs in the Portland area.

## Setting up for development

The easiest way to get set up is to install Docker and then run
`make docker-init` and then `make run-docker` (or just the latter, since
it will run the former). `docker-init` will create a service image for
Postgres with PostGIS installed and another image for GeoServer.

You can also set up a local dev environment by running `make init` as
usual. This is useful for running some commands locally even when using
Docker.

If you don't want to use Docker for development, you'll have to set up
Postgres and GeoServer manually.

From this point forward, it's assumed that `make run-docker` is running.
Alternatively, you can run `docker-compose up` directly.

### Testing

Run the following command:

    docker exec -it ecoroofs_ecoroofs_1 /webapps/ecoroofs/venv/bin/python manage.py test

### Migrations

Run the following command:

    docker exec -it ecoroofs_ecoroofs_1 /webapps/ecoroofs/venv/bin/python manage.py migrate

### Importing Data

Location data is stored in the git repo. Neighborhood data needs be
downloaded from Metro's RLIS Discovery site first:

    http://rlisdiscovery.oregonmetro.gov/?action=viewDetail&layerID=237

and extracted into `./rlis/nbo_hood`.

Then run the following command:

    docker exec -it ecoroofs_ecoroofs_1 /webapps/ecoroofs/venv/bin/inv configure -e docker import_all

### GeoServer

Unfortunately, you'll still need to go in and manually create some stuff
in GeoServer, but that's not *too* hard:

- Go to http://localhost:8080/geoserver/web/
- Log in with username `admin` and password `geoserver`
- Create a workspace named `ecoroofs`
- Create a PostGIS store in the `ecoroofs` workspace named `ecoroofs`
  - host: `database` (this is the host name configured via Docker
    Compose)
  - database: `ecoroofs`
  - user: `ecoroofs`
  - password: [leave blank]
- Create a `neighborhoods` layer from `ecoroofs:ecoroofs`
  - Find the `neighborhoods_neighborhood` table in the list and click the
    `Publish` link
  - Set the layer's name to `neighborhoods`
  - Set the layer's title to `Neighborhoods`
  - Click the `Compute from data` and `Compute from native bounds` links
- Create a `locations` layer from `ecoroofs:ecoroofs`. Because the
  location table has multiple geometry fields, this requires creating a
  "view" in GeoServer.
  - Go to the `Layers` page
  - Click the `Add new resource` link
  - From the `Add layer from` dropdown select `ecoroofs:ecoroofs`
  - Click the `Configure new SQL view...` link
  - Set the `View name` to `locations`
  - Set `SQL statement` to
    `select id, point_obscured from locations_location`
  - In the `Attributes` section, click the `Refresh` link
  - Set `Type` to `Point` and `SRID` to `4326` for the `point_obscured`
    attribute
  - `Save` (this will take you to the `Edit Layer` page)
  - Set the layer `Title` to `Locations`
  - Click the `Compute from data` and `Compute from native bounds` links
  - `Save` (this will take you back to the `Layers` page)
  
  ### Front End Tools
  
There is a `gulpfile.js` located in /ecoroofs/static/ that contains two helpful tasks. 
  
 - gulp-sass: Precompiles scss files
 - browserSync: Watches for changes to any file contained in the `static` directory and auto-reloads the active browser window
 
 Run `gulp watch` from within the static directory and a new browswer window will launch the application at http://localhost:3000. 
