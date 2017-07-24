import logging

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.gis.db.models import PointField

from ..models import BaseModel
from ..neighborhoods.models import Neighborhood


__all__ = [
    'Location',
    'BuildingUse',
    'Contractor',
    'Watershed',
    'ConstructionType',
    'Confidence',
]


log = logging.getLogger(__name__)


class Location(BaseModel):
    """
    Model for all eco-roof locations.
    Certain fields should not be exposed to the public including:
    point and address. An obscured field is used for these instead.
    """

    point = PointField()
    point_obscured = PointField()

    address = models.TextField(
        null=True, blank=True, verbose_name='exact street address')
    address_obscured = models.TextField(
        null=True, blank=True, verbose_name='obscured street address',
        help_text='This street address is available to the public.')

    composition = models.TextField(null=True, blank=True)
    depth_min = models.DecimalField(
        null=True, blank=True, decimal_places=1, max_digits=5,
        verbose_name='Minimum depth in inches')
    depth_max = models.DecimalField(
        null=True, blank=True, decimal_places=1, max_digits=5,
        verbose_name='Maximum depth in inches')
    drainage = models.TextField(null=True, blank=True)
    irrigated = models.NullBooleanField()
    maintenance = models.TextField(null=True, blank=True)
    number_of_roofs = models.PositiveIntegerField(
        default=1, verbose_name='Number of unique roofs at this location')
    plants = models.TextField(null=True, blank=True)
    solar_over_ecoroof = models.NullBooleanField()
    square_footage = models.PositiveIntegerField(null=True)
    year_built = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Year built')

    # Related fields
    building_use = models.ForeignKey('BuildingUse')
    confidence = models.ForeignKey('Confidence', null=True, blank=True)
    construction_type = models.ForeignKey('ConstructionType', null=True, blank=True)
    contractor = models.ForeignKey('Contractor', null=True, blank=True)
    neighborhood = models.ForeignKey('neighborhoods.Neighborhood', null=True, editable=False)
    watershed = models.ForeignKey('Watershed', null=True, blank=True)

    # Audit fields
    last_modified_on = models.DateTimeField(auto_now=True)

    def set_neighborhood_automatically(self):
        """Set neighborhood via spatial contains query.

        Finds the neighborhood (or neighborhoods) this Location is
        contained in. If it's in multiple neighborhoods, the first one
        returned from the database (ordered by name) will be used.

        """
        q = Neighborhood.objects.filter(geom__contains=self.point)
        neighborhood = q.first()
        if q.count() > 1:
            neighborhoods = q.all()
            log.warn('Location "%s" is in multiple neighborhoods: %s', self, neighborhoods)
        self.neighborhood = neighborhood

    def __str__(self):
        return '{self.name} at {self.point.y}, {self.point.x}'.format_map(locals())


@receiver(pre_save, sender=Location)
def set_neighborhood(sender, instance: Location, **kwargs):
    instance.set_neighborhood_automatically()


class BuildingUse(BaseModel):

    pass


class Composition(BaseModel):

    pass


class Contractor(BaseModel):

    pass


class Watershed(BaseModel):

    pass


class ConstructionType(BaseModel):

    pass


class Confidence(BaseModel):

    pass
