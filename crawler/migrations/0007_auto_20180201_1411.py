# Generated by Django 2.0.1 on 2018-02-01 14:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0006_auto_20180201_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 1, 14, 11, 23, 126291, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='price',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
