# Generated by Django 2.0.1 on 2018-02-13 12:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0008_auto_20180201_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 13, 12, 36, 32, 859494, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='deffects',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='engine',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
