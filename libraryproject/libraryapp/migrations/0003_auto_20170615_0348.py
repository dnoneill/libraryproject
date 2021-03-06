# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 03:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0002_auto_20170614_0132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=2000, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='author_id',
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.Author'),
        ),
    ]
