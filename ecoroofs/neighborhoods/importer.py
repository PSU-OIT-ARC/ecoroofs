from django.db import transaction
from django.db.models.signals import pre_save
from django.contrib.gis.utils import LayerMapping

from ecoroofs.neighborhoods.models import Neighborhood, normalize_name


class Importer:

    def __init__(self, path, from_srid=None, overwrite=False, dry_run=False, quiet=False):
        self.path = path
        self.from_srid = from_srid
        self.overwrite = overwrite
        self.dry_run = dry_run
        self.real_run = not dry_run
        self.quiet = quiet

    def run(self):
        if self.overwrite:
            print('Removing existing neighborhoods...', end='')
            if self.real_run:
                Neighborhood.objects.all().delete()
            print('Done')

        # Disconnect this temporarily so that the ``unique='name'`` option
        # passed to LayerMapping will work correctly (it collects all
        # records from the RLIS neighborhoods shapefile with the same name
        # into a single database record; if we normalize the names on save,
        # this feature won't work).
        pre_save.disconnect(normalize_name, sender=Neighborhood)

        print('Adding neighborhoods...', end='')
        if self.real_run:
            mapping = LayerMapping(
                Neighborhood, self.path, Neighborhood.layer_mapping, source_srs=self.from_srid,
                unique='name')
            mapping.save(strict=True)
        print('Done')

        print('Normalizing neighborhood names...', end='')
        neighborhoods = Neighborhood.objects.all()
        if self.real_run:
            with transaction.atomic():
                for neighborhood in neighborhoods:
                    neighborhood.name = Neighborhood.normalize_name(neighborhood.name)
                    neighborhood.save()
        print('Done')

        pre_save.connect(normalize_name, sender=Neighborhood)
