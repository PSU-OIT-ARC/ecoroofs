import uuid

import django.db.models.deletion
from django.db import migrations, models

import ecoroofs.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_add_neighborhood_field_to_location_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watershed',
            fields=[
                ('id', ecoroofs.models.UUIDPrimaryKeyField(default=uuid.uuid4, serialize=False)),
                ('slug', ecoroofs.models.UniqueDerivedSlugField(blank=True, editable=False, max_length=255)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='location',
            name='watershed',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Watershed'),
        ),
    ]
