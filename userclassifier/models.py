from __future__ import unicode_literals

from django.db import models

class ClassifierData(models.Model):
	classifierid = models.AutoField(primary_key=True)
	classifierp = models.CharField(max_length=100) 
	user = models.IntegerField()
	inputset = models.CharField(max_length=25000)
	outputset = models.CharField(max_length=1500)