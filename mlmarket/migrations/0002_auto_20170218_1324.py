# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlmarket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifierspre',
            name='classifierp',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classifierspre',
            name='name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
