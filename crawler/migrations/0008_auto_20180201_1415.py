# Generated by Django 2.0.1 on 2018-02-01 14:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0007_auto_20180201_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 1, 14, 15, 51, 305720, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='odometr_value',
            field=models.CharField(max_length=20, null=True),
        ),
    ]