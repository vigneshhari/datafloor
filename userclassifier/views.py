from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max
from django.http import HttpResponseRedirect
from models import ClassifierData
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
import cPickle as pickle
import numpy as np
import random
import datetime
import time 
import os
import csv



def upload(request):
	if(request.method != "POST"):
		return render(request,"uploadpage.html")
	file = request.FILES['data']
	if not os.path.exists('upload/'):
	    os.mkdir('upload/')
	
	classifierp = ''.join(random.choice('0123456789ABCDEF') for i in range(16)) #This creates a random String of letters Used for Unique Identity
	
	temp = ClassifierData(classifierp = classifierp , user = 1)
	temp.save()

	with open('upload/' + classifierp , 'wb+') as destination:
	    for chunk in file.chunks():
	        destination.write(chunk)

	with open('upload/' + classifierp ) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		readCSV = list(readCSV)
		headings = readCSV[0]

	print headings
	return render(request,"inputdata.html",{"input":headings , "key" : classifierp , "id" : temp.classifierid})

def updateclass(request):
	print request.POST.keys()
	xval = []
	yval = request.POST['y']
	for i in request.POST.keys():
		if(request.POST[i] == "x"):
			xval.append(i.encode('utf8'))
	xval.sort()
	print xval , yval
	temp = ClassifierData.objects.all().filter(classifierid = request.POST['classifierid']).update(inputset = ','.join(xval) , outputset = yval)
	return render(request,"classuploaded.html", {"key" : request.POST['key'] , "id" : request.POST['classifierid']  })

def train(request):
	classifierid = request.GET.get('id','-1')
	key = request.GET.get('key','-1')
	temper = ''
	check = ClassifierData.objects.all().filter(classifierid =  classifierid)
	for i in check:
		temper = i.classifierp
		x_val = i.inputset.split(",")
		y_val = i.outputset
	if(temper != key):
		return JsonResponse( {"Authentication" : "Failed"})
	client = MongoClient()
	db = client.userclassifier
	if(classifierid not in db.collection_names()):
		with open('upload/' + key) as csvfile:
			infos = db[classifierid]
			readCSV = csv.reader(csvfile, delimiter=',')
			readCSV = list(readCSV)
			headings = readCSV[0]
			
			datas = readCSV[1:]
		l = []
		for index, data in enumerate(datas):
			l.append(dict(zip(headings,data)))
		infos.insert_many(l)	
	infos = db[classifierid]
	xunf = {}
	for i in x_val:
		xunf[i] = []

	file = open(  'upload/' + key + ".p", "wb" )

	finaly = []

	for info in infos.find():
		finaly.append(info[y_val].encode('utf8'))
		looper= 0
		for i in x_val:
			try:
				xunf[i].append(float(info[i].encode('utf8')))
			except Exception as e :
				xunf[i].append(info[i].encode('utf8'))

	ykey = []
	
	for i in finaly:
		try:
			pp =  float(i)
		except:
			ykey =  list(set(finaly))
			finaly = [ykey.index(val) for val in finaly]
			break

	xkey = {}

	for x in xunf.keys():
		for i in xunf[x]: 
			try:
				pp =  float(i)
			except:
				keys =  list(set(xunf[x]))
				xkey[x] = keys
				temp = [keys.index(val) for val in xunf[x]]
				xunf[x] = temp
				break
	finalx = []


	for i in range(0,len(xunf.values()[0])):
		temp = []
		for k in xunf.values():
			temp.append(k[i])
		finalx.append(temp)
	
	print xkey.keys()
	print finalx[0]
	print finalx[1]
	regr = RandomForestClassifier()
	regr.fit(finalx[:(9 * len(finalx) / 10 )], finaly[:(9 * len(finaly) / 10 )])

	pickle.dump(regr , file)
	pickle.dump(xkey , file)
	pickle.dump(ykey , file)

	acc =  regr.score(finalx[(9 * len(finalx) / 10 ):],finaly[(9 * len(finalx) / 10 ):]) * 100 

	print acc 

	return JsonResponse( {"training Accuracy" : str( acc ) }) 

def classify(request):
	classifierid = request.GET.get('id','-1')
	key = request.GET.get('key','-1')
	temper = ''
	check = ClassifierData.objects.all().filter(classifierid =  classifierid)
	for i in check:
		temper = i.classifierp
		x_val = i.inputset.split(",")
		print x_val
		y_val = i.outputset
	if(temper != key):
		return JsonResponse( {"Authentication" : "Failed"})
	for i in x_val:
		if (i not in request.GET.keys()):
			return JsonResponse({"Input Data Not Sufficient" : "ERROR"})
	temp = open('upload/' + key + ".p", "rb")
	regr = pickle.load(temp)
	xkey = pickle.load(temp)
	ykey = pickle.load(temp)
	
	inpdata = []

	print xkey

	for x in x_val:
		try:
			print "hello"
			print xkey[x]
			inpdata.append(xkey[x].index(request.GET.get(x.strip())))
			print "again"
		except:
			inpdata.append(request.GET.get(x.strip()))
	

	print inpdata
	
	predictedval = regr.predict(inpdata)


	if(ykey == []):
		return JsonResponse({y_val : str(predictedval)})
	
	return JsonResponse({y_val : ykey[predictedval]}) 





