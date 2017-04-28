import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0007_add_year_built_to_location_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='point_obscured',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
    ]
