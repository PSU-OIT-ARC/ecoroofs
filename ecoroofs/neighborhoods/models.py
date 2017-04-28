import re

from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..models import BaseModel


class Neighborhood(BaseModel):

    class Meta:
        ordering = ['name']

    objects = models.GeoManager()

    layer_mapping = {
        'name': 'NAME',
        'area': 'AREA',
        'geom': 'MULTIPOLYGON',
    }

    name = models.CharField(max_length=255)
    area = models.FloatField()
    geom = models.MultiPolygonField()

    @classmethod
    def normalize_name(cls, name):
        splitters = ' /-'

        name = name.lower()
        name = re.sub(r'\bpdx\b', 'PDX', name, re.I)
        name = re.sub(r'\bcpo\b', 'CPO', name, re.I)
        name = re.sub(r'\s+', ' ', name)
        name = re.sub(r'\s*/\s*', '/', name)
        name = re.sub(r'\s*-\s*', '-', name)

        collector = []
        for i, c in enumerate(name, -1):
            p = '' if i == -1 else name[i]
            if p in splitters:
                c = c.upper()
            collector.append(c)

        normalized_name = ''.join(collector)
        return normalized_name


@receiver(pre_save, sender=Neighborhood)
def normalize_name(sender, instance, **kwargs):
    instance.name = instance.normalize_name(instance.name)
