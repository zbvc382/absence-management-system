# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-08 18:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_calendarrestrictionprivate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CalendarRestrictionPrivate',
            new_name='CalendarRestriction',
        ),
    ]
