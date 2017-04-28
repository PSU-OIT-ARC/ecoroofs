from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0013_add_construction_type_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='exact street address'),
        ),
    ]
