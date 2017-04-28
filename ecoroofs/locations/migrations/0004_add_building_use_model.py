import uuid

import django.db.models.deletion
from django.db import migrations, models

import ecoroofs.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_add_watershed_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingUse',
            fields=[
                ('id', ecoroofs.models.UUIDPrimaryKeyField(default=uuid.uuid4, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', ecoroofs.models.UniqueDerivedSlugField(blank=True, editable=False, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='location',
            name='building_use',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.BuildingUse'),
        ),
    ]
