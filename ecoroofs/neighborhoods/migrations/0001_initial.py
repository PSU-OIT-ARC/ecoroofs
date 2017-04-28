import uuid

import django.contrib.gis.db.models.fields
from django.db import migrations, models

import ecoroofs.models


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', ecoroofs.models.UUIDPrimaryKeyField(default=uuid.uuid4, serialize=False)),
                ('slug', ecoroofs.models.UniqueDerivedSlugField(blank=True, editable=False, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
