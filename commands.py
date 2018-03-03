from runcommands import command
from runcommands.util import abort, abs_path, args_to_str, printer

from emcee.commands import *
from emcee.commands.deploy import deploy

from emcee.backends.dev.db import provision_database as provision_database_local
from emcee.backends.aws.provision.python import provision_python
from emcee.backends.aws.provision.gis import provision_gis
from emcee.backends.aws.provision.services.local import provision_nginx
from emcee.backends.aws.provision.services.remote import provision_database
from emcee.backends.aws.deploy import AWSDjangoDeployer
from emcee.backends.aws.infrastructure.commands import *


@command(env='dev', timed=True)
def init(config, overwrite=False, drop_db=False):
    virtualenv(config, overwrite=overwrite)
    install(config)
    npm_install(config, where='{package}:static', modules=[])
    # provision_database_local(config, drop=drop_db, with_postgis=True)
    manage(config, 'migrate --no-input')
    sass(config)
    # test(config, force_env='test')


@command(env='dev')
def build_static(config, css=True, css_sources=(), js=True, js_sources=(),
                 optimize=True, static_root=None, echo=False, hide=None):
    if css:
        build_css(config, sources=css_sources, optimize=optimize, echo=echo, hide=hide)
    if js:
        build_js(config, sources=js_sources, echo=echo, hide=hide)
    manage(config, 'collectstatic', '--noinput')


# TODO: Is this definition necessary (i.e., will it work with the imported 'build_js'?)
# @command(env='dev', timed=True)
# def build_js(config, sources=(), echo=False, hide=None):
#     # TODO: Pass sources to Node script?
#     if sources:
#         abort(1, 'The --sources option is currently ignored by build_js')
#     where = abs_path(args_to_str('{package}:static', format_kwargs=config))
#     local(config, ('node', 'build.js'), cd=where, echo=echo, hide=hide)


# @command(default_env='dev', timed=True)
# def import_all(config, reset_db=False,
#                neighborhoods_shapefile_path='rlis/nbo_hood', from_srid=None,
#                locations_file_name='locations.csv',
#                overwrite=False, dry_run=False, quiet=False):
#     if reset_db:
#         reset_db(config)
#         manage(config, 'migrate')
#     import_neighborhoods(
#         config, neighborhoods_shapefile_path, from_srid, overwrite, dry_run, quiet)
#     import_locations(config, locations_file_name, overwrite, dry_run, quiet)


# @command(default_env='dev', timed=True)
# def import_locations(config, file_name='locations.csv', overwrite=False, dry_run=False,
#                      quiet=False):
#     """Import locations from CSV file provided by client."""
#     from emcee.commands.django import setup; setup(config)  # noqa
#     from ecoroofs.locations.importer import Importer
#     location_importer = Importer(file_name, overwrite=overwrite, dry_run=dry_run, quiet=quiet)
#     location_importer.run()


# @command(default_env='dev', timed=True)
# def import_neighborhoods(config, path='rlis/nbo_hood', from_srid=None,
#                          overwrite=True, dry_run=False, quiet=False):
#     """Import neighborhoods from RLIS shapefile.

#     We overwrite by default because doing so should be safe.

#     The neighborhoods shapefile can be downloaded from Metro's RLIS
#     Discovery site::

#         http://rlisdiscovery.oregonmetro.gov/?action=viewDetail&layerID=237

#     This task expects the shapefile directory to be at ``rlis/nbo_hood``
#     by default, but it can be located anywhere if you pass the
#     corresponding ``--path`` option.

#     """
#     from emcee.django import setup; setup(config)  # noqa
#     from ecoroofs.neighborhoods.importer import Importer
#     location_importer = Importer(
#         path, from_srid=from_srid, overwrite=overwrite, dry_run=dry_run, quiet=quiet)
#     location_importer.run()


# class Deployer(AWSPythonDeployer):
#     def build_static(self):
#         printer.header('Building static files (EcoRoofs custom)...')
#         build_static(self.config, static_root='{path.build.static_root}')


@command(env=True)
def deploy_app(config, provision=False, createdb=False):
    if provision:
        provision_python(config)
        provision_gis(config)
        provision_nginx(config)
    if createdb:
        provision_database(config, with_postgis=True,
                           extensions=['postgis', 'hstore'])

    deploy(config, deployer_class=AWSDjangoDeployer)
