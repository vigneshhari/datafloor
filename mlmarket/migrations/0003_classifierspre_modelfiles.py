# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlmarket', '0002_auto_20170218_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifierspre',
            name='modelfiles',
            field=models.CharField(default=0, max_length=500),
            preserve_default=False,
        ),
    ]
