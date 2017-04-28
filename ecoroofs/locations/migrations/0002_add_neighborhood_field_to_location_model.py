from django.db import migrations, models
import django.db.models.deletion


def set_neighborhoods(apps, schema_editor):
    location_model = apps.get_model('locations', 'Location')
    locations = location_model.objects.all()
    for location in locations:
        location.save()


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('neighborhoods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='neighborhood',
            field=models.ForeignKey(null=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to='neighborhoods.Neighborhood'),
        ),

        migrations.RunPython(set_neighborhoods)
    ]
