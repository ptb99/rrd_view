# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volts', '0002_auto_20180126_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='axis_label',
            field=models.CharField(default='Volts', max_length=128),
        ),
        migrations.AddField(
            model_name='graph',
            name='lower',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='graph',
            name='upper',
            field=models.FloatField(default=20.0),
        ),
        migrations.AddField(
            model_name='graph',
            name='value_field',
            field=models.CharField(default='voltage', max_length=128),
        ),
    ]
