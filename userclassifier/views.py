from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max
from django.http import HttpResponseRedirect
from .models import ClassifierData
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np
import random
import datetime
import time 
import os
import csv
from classifier.views import classifier
from classifier.models import classifiers


def upload(request):
    id = request.session.get('userid', "")
    if (id == ""):
        return HttpResponseRedirect("/home")
    if(request.method != "POST"):
        return render(request,"uploadpage.html")
    file = request.FILES['data']
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    cl = classifiers.objects.all()
    cdata = []
    for i in cl:
        cdata.append(i.classifier)

    classifierp = ''.join(random.choice('0123456789ABCDEF') for i in range(16)) #This creates a random String of letters Used for Unique Identity
	
    temp = ClassifierData(classifierp = classifierp , user = id , type="user" , classifier="Knn"  )
    temp.save()

    with open('upload/' + classifierp , 'wb+') as destination:
    	if file.multiple_chunks:
    		for c in file.chunks():
    			destination.write(c)
    	else:
    		destination.write(file.read())

    with open('upload/' + classifierp ) as csvfile:
    	readCSV = csv.reader(csvfile, delimiter=',')
    	readCSV = list(readCSV)
    	headings = readCSV[0]


    return render(request,"inputdata.html",{"classifier" : cdata , "input":headings , "key" : classifierp , "id" : temp.classifierid })

def updateclass(request):
    id = request.session.get('userid', "")
    if (id == ""):
        return HttpResponseRedirect("/home")
    xval = []
    yval = request.POST["y"]
    for i in request.POST.keys():
    	if(request.POST[i] == "on"):
    		xval.append(i)
    xval.sort()
    name = request.POST.get("name" ,"")
    if( name == ""):
        name = "Classifier#" + request.POST['key']
    temp = ClassifierData.objects.all().filter(classifierid = request.POST['classifierid']).update(classifier = request.POST['classifier'],type="user",name = name,inputset = ','.join(xval) , outputset = yval)
    return render(request,"classuploaded.html", {"y":yval ,"x" : xval ,"classifiername" : name,"sucess" :1 ,"key" : request.POST['key'] , "id" : request.POST['classifierid']  })

def train(request):
    classifierid = request.GET.get('id','-1')
    key = request.GET.get('key','-1')
    temper = ''
    check = ClassifierData.objects.all().filter(classifierid =  classifierid)
    for i in check:
        classname = i.classifier
        x = i.inputset
        type = i.type
        temper = i.classifierp
        x_val = i.inputset.split(",")
        y_val = i.outputset
    if(temper != key):
        return JsonResponse( {"Authentication" : "Failed"})
    out = classifier(classifierid , key , type , "train" , classname , None , x , y_val )
    return JsonResponse(out.perform())

def classify(request):
    classifierid = request.GET.get('id','-1')
    key = request.GET.get('key','-1')
    temper = ''
    type = ""
    classname = ""
    check = ClassifierData.objects.all().filter(classifierid =  classifierid)
    for i in check:
        temper = i.classifierp
        x = i.inputset
        classname = i.classifier
        x_val = i.inputset.split(",")
        type = i.type
        y_val = i.outputset
    if(temper != key):
        return JsonResponse( {"Authentication" : "Failed"})
    input = {}
    for i in x_val:
        input[i] = request.GET.get(i)
        if (i not in request.GET.keys()):
            return JsonResponse({"Input Data Not Sufficient" : "ERROR"})

    out = classifier(classifierid , key , type , "classify" , classname ,input , x , y_val )
    return JsonResponse(out.perform())

def details(request):
    id = request.session.get('userid', "")
    if (id == ""):
        return HttpResponseRedirect("/home")
    data = ClassifierData.objects.all().filter(classifierid = request.GET.get("id" , 0))
    uesr = ""
    for i in data:
        user = i.user
    if(user != id):
        return HttpResponseRedirect('/dashboard')
    for i in data:
        return render(request,"classuploaded.html", {"y":i.outputset ,"x" : i.inputset.split(",") ,"classifiername" : i.name ,"key" : i.classifierp , "id" : i.classifierid  })









