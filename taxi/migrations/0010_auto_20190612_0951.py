# Generated by Django 2.2.1 on 2019-06-12 05:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0009_auto_20190612_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 12, 9, 51, 59, 400543)),
        ),
    ]