from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0010_add_number_of_roofs_field_to_location_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='solar_over_ecoroof',
            field=models.NullBooleanField(),
        ),
    ]
