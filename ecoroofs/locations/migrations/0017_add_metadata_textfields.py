import uuid

from django.db import migrations, models

import ecoroofs.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0016_add_confidence__model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Composition',
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
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='drainage',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='maintenance',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='plants',
            field=models.TextField(blank=True, null=True),
        ),
    ]
