# Generated by Django 2.1.5 on 2019-02-23 20:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20190223_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playeruser',
            name='regTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 23, 20, 57, 25, 719359, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='playeruser',
            name='time',
            field=models.FloatField(default=400.0),
        ),
    ]
