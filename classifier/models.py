from __future__ import unicode_literals

from django.db import models


class classifiers(models.Model):
    classifierid = models.AutoField(primary_key=True)
    classifier = models.CharField(max_length=100)

