# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_customercontact_equipmentdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentdetails',
            name='equipment_make',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
