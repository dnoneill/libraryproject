# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 21:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0005_auto_20170615_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='LOANS', to=settings.AUTH_USER_MODEL),
        ),
    ]
