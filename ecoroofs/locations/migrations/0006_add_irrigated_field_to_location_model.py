from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_add_square_footage_field_to_location_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='irrigated',
            field=models.NullBooleanField(),
        ),
    ]
