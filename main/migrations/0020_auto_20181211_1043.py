# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-12-11 06:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_movies_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.TimeField(default=datetime.date(2018, 12, 11)),
        ),
    ]