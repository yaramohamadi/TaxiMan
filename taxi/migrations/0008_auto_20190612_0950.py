# Generated by Django 2.2.1 on 2019-06-12 05:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0007_auto_20190612_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 12, 9, 50, 40, 169786)),
        ),
    ]
