# Generated by Django 2.2.1 on 2019-06-11 15:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 11, 19, 42, 30, 129545)),
        ),
    ]
