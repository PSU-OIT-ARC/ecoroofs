from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0011_add_solar_over_ecoroof_field_to_location_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='depth_max',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Maximum depth in inches'),
        ),
        migrations.AddField(
            model_name='location',
            name='depth_min',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Minimum depth in inches'),
        ),
    ]
