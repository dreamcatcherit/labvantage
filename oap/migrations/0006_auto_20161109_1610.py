# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-09 10:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('oap', '0005_auto_20161107_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementalanalysis',
            name='user_id',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oilanalysis',
            name='user_id',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
