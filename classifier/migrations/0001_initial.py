# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='classifiers',
            fields=[
                ('classifierid', models.AutoField(primary_key=True, serialize=False)),
                ('classifier', models.CharField(max_length=100)),
            ],
        ),
    ]