from __future__ import unicode_literals

from django.db import models


class classifierspre(models.Model):
    classifierid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    classifier = models.CharField(max_length=100)
    inputset = models.CharField(max_length=500)
    outputset = models.CharField(max_length=500)
    modelfiles = models.CharField(max_length=500)
    desc = models.TextField()


