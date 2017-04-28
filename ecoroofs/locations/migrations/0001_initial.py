import uuid

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models

import ecoroofs.models


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', ecoroofs.models.UUIDPrimaryKeyField(default=uuid.uuid4, serialize=False)),
                ('slug', ecoroofs.models.UniqueDerivedSlugField(blank=True, editable=False, max_length=255)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
