import uuid

import django.db.models.deletion
from django.db import migrations, models

import ecoroofs.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0008_add_point_obscured_to_location_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', ecoroofs.models.UUIDPrimaryKeyField(default=uuid.uuid4, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', ecoroofs.models.UniqueDerivedSlugField(blank=True, editable=False, max_length=255)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='location',
            name='contractor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Contractor'),
        ),
    ]
