from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0017_add_metadata_textfields'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='last_modified_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
