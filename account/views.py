from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max
from django.http import HttpResponseRedirect
import random
import datetime
import time 
import hashlib
# Create your views here.

def login(request):
	return render(request,"login.html")