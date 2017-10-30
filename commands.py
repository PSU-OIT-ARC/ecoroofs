from runcommands import command
from runcommands.util import abort, abs_path, args_to_str, printer

from arctasks.dev import commands as dev
from arctasks.aws import commands as aws
from arctasks.aws.deploy import AWSDeployer

from arctasks.aws.commands import *


@command(env='dev', timed=True)
def init(config, overwrite=False, drop_db=False):
    dev.virtualenv(config, overwrite=overwrite)
    dev.install(config)
    dev.npm_install(config, where='{package}:static', modules=[])
    dev.createdb(config, drop=drop_db, with_postgis=True)
    dev.migrate(config)
    dev.sass(config)
    dev.test(config, force_env='test')


@command(env='dev')
def build_static(config, css=True, css_sources=(), js=True, js_sources=(), collect=True,
                 optimize=True, static_root=None, echo=False, hide=None):
    if css:
        dev.build_css(config, sources=css_sources, optimize=optimize, echo=echo, hide=hide)
    if js:
        dev.build_js(config, sources=js_sources, echo=echo, hide=hide)
    if collect:
        dev.collectstatic(config, static_root=static_root, echo=echo, hide=hide)


@command(env='dev', timed=True)
def build_js(config, sources=(), echo=False, hide=None):
    # TODO: Pass sources to Node script?
    if sources:
        abort(1, 'The --sources option is currently ignored by build_js')
    where = abs_path(args_to_str('{package}:static', format_kwargs=config))
    local(config, ('node', 'build.js'), cd=where, echo=echo, hide=hide)


@command(default_env='dev', timed=True)
def import_all(config, reset_db=False,
               neighborhoods_shapefile_path='rlis/nbo_hood', from_srid=None,
               locations_file_name='locations.csv',
               overwrite=False, dry_run=False, quiet=False):
    if reset_db:
        dev.reset_db(config)
        dev.migrate(config)
    import_neighborhoods(
        config, neighborhoods_shapefile_path, from_srid, overwrite, dry_run, quiet)
    import_locations(config, locations_file_name, overwrite, dry_run, quiet)


@command(default_env='dev', timed=True)
def import_locations(config, file_name='locations.csv', overwrite=False, dry_run=False,
                     quiet=False):
    """Import locations from CSV file provided by client."""
    from arctasks.django import setup; setup(config)  # noqa
    from ecoroofs.locations.importer import Importer
    location_importer = Importer(file_name, overwrite=overwrite, dry_run=dry_run, quiet=quiet)
    location_importer.run()


@command(default_env='dev', timed=True)
def import_neighborhoods(config, path='rlis/nbo_hood', from_srid=None,
                         overwrite=True, dry_run=False, quiet=False):
    """Import neighborhoods from RLIS shapefile.

    We overwrite by default because doing so should be safe.

    The neighborhoods shapefile can be downloaded from Metro's RLIS
    Discovery site::

        http://rlisdiscovery.oregonmetro.gov/?action=viewDetail&layerID=237

    This task expects the shapefile directory to be at ``rlis/nbo_hood``
    by default, but it can be located anywhere if you pass the
    corresponding ``--path`` option.

    """
    from arctasks.django import setup; setup(config)  # noqa
    from ecoroofs.neighborhoods.importer import Importer
    location_importer = Importer(
        path, from_srid=from_srid, overwrite=overwrite, dry_run=dry_run, quiet=quiet)
    location_importer.run()


class Deployer(AWSDeployer):
    def build_static(self):
        printer.header('Building static files (EcoRoofs custom)...')
        build_static(self.config, static_root='{path.build.static_root}')

    def post_install(self):
        from arctasks.remote import manage

        # Migrate database schema
        manage(self.config, 'migrate')


@command(env=True)
def deploy_app(config, provision=False, createdb=False):
    if provision:
        aws.provision_webhost(config, with_gis=True)
    if createdb:
        aws.createdb(config, with_postgis=True,
                     extensions=['postgis', 'hstore'])

    aws.deploy(config, deployer_class=Deployer)
