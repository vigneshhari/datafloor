from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max
from django.http import HttpResponseRedirect
from .models import User
from userclassifier.models import ClassifierData
import random
import datetime
import time 
import hashlib
# Create your views here.

def login(request):
	if(request.method != "POST"):
		return render(request,"login.html")
	password = hashlib.sha256((request.POST.get('password','').encode("utf8"))).hexdigest()
	email = request.POST.get("email")
	auth = User.objects.all().filter(email = email )
	userid = ""
	pwd= ""
	for i in auth:
		userid = i.user_id
		pwd = i.password
	if(pwd == password):
		request.session['userid'] = userid
		return HttpResponseRedirect("/dashboard")
	return render(request ,"login.html" , {"error" : "Username/Password Combination is Wrong"})
def signup(request):
	if(request.method != "POST"):
		return render(request,"signup.html")
	password = hashlib.sha256((request.POST.get('password','')).encode("utf8")).hexdigest() #Hasing Password For Better Security
	name = request.POST.get("name")
	phno = request.POST.get("phoneno")
	email = request.POST.get("email")
	if(request.POST.get("password") != request.POST.get("cpassword")):return render(request, "signup.html", {"error": "Passwords Dont Match"})
	auth = User.objects.all().filter(email = email )
	for i in auth:
		return render(request, "signup.html", {"error": "Email Id Already registered with Datafloor"})
	data = User(name = name , password = password , email = email , phone_no = phno , verified = 0)
	data.save()
	return render(request ,"login.html" , {"error" : "Account Registered . Please Login to continue"})

def dash(request):
	id = request.session.get('userid',"")
	if(id == ""):
		return HttpResponseRedirect("/home")
	userdata = User.objects.all().filter(user_id=id)
	name=""
	for i in userdata:
		name = i.name
	cdata = ClassifierData.objects.all().filter(user = id)
	tclass = 0
	uclass = 0
	pclass = 0
	data = []
	k=0
	for i in cdata:
		k = k+1
		data.append({"no":k,"name" : i.name , "classifier" : i.classifier , "url" : "/details?id=" + str(i.classifierid)  })
		tclass = tclass +1
		if(type == "user") : uclass = uclass+1
		else: pclass = pclass+1

	return render(request,"dashboard.html",{"data" : data , "name" : name , "req" : "--" , "classifer" : tclass , "tclassifier" : uclass , "mclassifer" : pclass})

def logout(request):
	request.session["userid"] = ""
	return HttpResponseRedirect("/home")