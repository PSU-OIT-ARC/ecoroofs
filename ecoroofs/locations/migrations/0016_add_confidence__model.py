import uuid

from django.db import migrations, models
import django.db.models.deletion

import ecoroofs.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0015_add_address_obscured_field_to_location_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confidence',
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
            name='confidence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Confidence'),
        ),
    ]
