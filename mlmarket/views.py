from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max
from pymongo import MongoClient
from sklearn.neighbors import KNeighborsClassifier
from django.http import HttpResponseRedirect
from userclassifier.models import ClassifierData
from sklearn.ensemble import RandomForestClassifier
import pickle
import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier



from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
import time
import numpy as np
import random
import datetime
import time
import os
import csv
from .models import classifierspre
from userclassifier.models import ClassifierData
# Create your views here.

def market(request):
    id = request.session.get('userid', "")
    if (id == ""):
        return HttpResponseRedirect("/home")
    classifiers = classifierspre.objects.all()
    data = []
    k = 0;
    for i in classifiers:
        k = k+1
        data.append({"name" : i.name , "url" : ("/mview?id=" + str(i.classifierid)) ,"desc" : i.desc[:40],"no":k})
    print(data)
    return render(request,"market.html" , {"data" : data})

def addclass(request):
    id = request.session.get('userid', "")
    if (id == ""):
        return HttpResponseRedirect("/home")
    cdata = classifierspre.objects.all().filter(classifierid=request.GET.get("id",0))
    for i in cdata:
        obj = ClassifierData(name=i.name ,classifierp=''.join(random.choice('0123456789ABCDEF') for i in range(16)) , classifier=i.classifier , inputset=i.inputset , outputset=i.outputset ,type="pre" , user=id).save()
        return HttpResponseRedirect("/dashboard")

def mview(request):
    id = request.session.get('userid', "")
    if (id == ""):
        return HttpResponseRedirect("/home")
    classifiers = classifierspre.objects.all().filter(classifierid=request.GET.get("id",0))
    for i in classifiers:
        return render(request, "marketview.html", {"name" : i.name , "url" : ("/addclass?id=" + str(i.classifierid)) ,"desc" : i.desc})
