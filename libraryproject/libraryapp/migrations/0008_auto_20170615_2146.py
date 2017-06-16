# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 21:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0007_auto_20170615_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='libraryapp.Book'),
        ),
    ]