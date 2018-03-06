from django.core.management.base import BaseCommand, CommandError
from ecoroofs.neighborhoods.importer import Importer


class Command(BaseCommand):
    """Import neighborhoods from RLIS shapefile.

    We overwrite by default because doing so should be safe.

    The neighborhoods shapefile can be downloaded from Metro's RLIS
    Discovery site::

        http://rlisdiscovery.oregonmetro.gov/?action=viewDetail&layerID=237

    This task expects the shapefile directory to be at ``rlis/nbo_hood``
    by default, but it can be located anywhere if you pass the
    corresponding ``--path`` option.

    """
    help = 'Imports neighborhoods from the given RLIS shapefile.'

    def add_arguments(self, parser):
        parser.add_argument('path', help='The path to the RLIS shapefile')
        parser.add_argument('--from-srid', action="store", dest="from_srid",
                            help="Use the given SRID")
        parser.add_argument('--overwrite', action="store_true", dest="overwrite",
                            default=True,
                            help="Overwrite existing data.")
        parser.add_argument('--dry-run', action="store_true", dest="dry_run")
        parser.add_argument('--quiet', action="store_true", dest="quiet")

    def handle(self, *args, **options):
        location_importer = Importer(options.get('path'),
                                     from_srid=options.get('from_srid'),
                                     overwrite=options.get('overwrite'),
                                     dry_run=options.get('dry_run'),
                                     quiet=options.get('quiet'))
        location_importer.run()
