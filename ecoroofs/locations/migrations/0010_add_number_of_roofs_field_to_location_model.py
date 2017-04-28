from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0009_add_contractor_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='number_of_roofs',
            field=models.PositiveIntegerField(default=1, verbose_name='Number of unique roofs at this location'),
        ),
    ]
