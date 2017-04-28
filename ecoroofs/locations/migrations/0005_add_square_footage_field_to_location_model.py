from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_add_building_use_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='square_footage',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
