from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max
from django.http import HttpResponseRedirect
from models import User 
import random
import datetime
import time 
import hashlib
# Create your views here.

def login(request):
	if(request.method != "POST"):
		return render(request,"login.html")
	password = request.POST.get("password")
	email = request.POST.get("email")
	auth = User.objects.all().filter(email = email )
	for i in auth:
		pwd = i.password
	if(pwd == password):
		return JsonResponse({"Authentication":"Sucessful"})
	return JsonResponse({"Authentication":"Failed"})
def signup(request):
	if(request.method != "POST"):
		return render(request,"signup.html")
	password = request.POST.get("password")
	name = request.POST.get("name")
	phno = request.POST.get("phoneno")
	email = request.POST.get("email")
	data = User(name = name , password = password , email = email , phone_no = phno , verified = 0)
	data.save()
	return JsonResponse({"Name" : name , "Password" : password , "Email" : email , "Phone Number" : phno })
