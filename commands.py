from runcommands import command
from runcommands.util import abort, abs_path, args_to_str, printer

from arctasks.commands import *
from arctasks.deploy import Deployer


@command(env='dev', timed=True)
def init(config, overwrite=False, drop_db=False):
    virtualenv(config, overwrite=overwrite)
    install(config)
    npm_install(config, where='{package}:static', modules=[])
    createdb(config, drop=drop_db)
    migrate(config)
    sass(config)
    test(config, force_env='test')


@command(env='dev')
def build_static(config, css=True, css_sources=(), js=True, js_sources=(), collect=True,
                 optimize=True, static_root=None, echo=False, hide=None):
    if css:
        build_css(config, sources=css_sources, optimize=optimize, echo=echo, hide=hide)
    if js:
        build_js(config, sources=js_sources, echo=echo, hide=hide)
    if collect:
        collectstatic(config, static_root=static_root, echo=echo, hide=hide)


@command(env='dev', timed=True)
def build_js(config, sources=(), echo=False, hide=None):
    # TODO: Pass sources to Node script?
    if sources:
        abort(1, 'The --sources option is currently ignored by build_js')
    where = abs_path(args_to_str('{package}:static', format_kwargs=config))
    local(config, ('node', 'build.js'), cd=where, echo=echo, hide=hide)


class EcoRoofsDeployer(Deployer):

    def build_static(self):
        printer.header('Building static files (EcoRoofs custom)...')
        build_static(self.config, static_root='{path.build.static_root}')


deploy.deployer_class = EcoRoofsDeployer


@command(default_env='dev', timed=True)
def import_all(config, reset_db=False,
               neighborhoods_shapefile_path='rlis/nbo_hood', from_srid=None,
               locations_file_name='locations.csv',
               overwrite=False, dry_run=False, quiet=False):
    if reset_db:
        reset_db(config)
        migrate(config)
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
