from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0014_add_address_field_to_location_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='address_obscured',
            field=models.TextField(blank=True, help_text='This street address is available to the public.', null=True, verbose_name='obscured street address'),
        ),
    ]
