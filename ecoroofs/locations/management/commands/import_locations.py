from django.core.management.base import BaseCommand, CommandError

from ecoroofs.neighborhoods.models import Neighborhood
from ecoroofs.locations.importer import Importer


class Command(BaseCommand):
    help = 'Imports locations from the given CSV.'

    def add_arguments(self, parser):
        parser.add_argument('csv', help='The CSV to use for importing')
        parser.add_argument('--overwrite', action="store_true", dest="overwrite",
                            help="Overwrite existing data.")
        parser.add_argument('--dry-run', action="store_true", dest="dry_run")
        parser.add_argument('--quiet', action="store_true", dest="quiet")

    def handle(self, *args, **options):
        if not Neighborhood.objects.exists():
            raise CommandError('Neighborhoods must first be imported.')

        location_importer = Importer(options.get('csv'),
                                     overwrite=options.get('overwrite'),
                                     dry_run=options.get('dry_run'),
                                     quiet=options.get('quiet'))
        location_importer.run()
