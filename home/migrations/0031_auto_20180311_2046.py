# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-11 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_auto_20180311_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='link',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]