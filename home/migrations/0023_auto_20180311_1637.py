# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-11 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_auto_20180311_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
