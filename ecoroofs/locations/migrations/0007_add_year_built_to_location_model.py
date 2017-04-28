from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_add_irrigated_field_to_location_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='year_built',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Year built'),
        ),
    ]
