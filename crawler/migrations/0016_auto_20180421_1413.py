# Generated by Django 2.0.1 on 2018-04-21 14:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0015_auto_20180401_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 21, 14, 13, 25, 382873, tzinfo=utc)),
        ),
    ]
