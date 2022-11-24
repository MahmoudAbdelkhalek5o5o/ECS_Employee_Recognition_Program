from django.shortcuts import render
from asyncio.windows_events import NULL
from contextlib import nullcontext
from pydoc import describe
from unicodedata import category
from urllib import request
from django.shortcuts import render, redirect
from datetime import datetime,date,timedelta
from django.core.mail import send_mail

from .models import  ActivityRequest, ActivityRequest, Activity, ActivityCategory ,Points,ActivitySuggestion
from Users.models import User ,announcement , ROLE
from Rewards.models import budget , Suggest_vendor
import pytz
from django.forms.models import model_to_dict

# Create your views here.
def suggest_activity(request):
        categories= ActivityCategory.objects.filter(is_archived = False)
        if request.method== "POST":
            if not request.user.role == ROLE[0][0]:
                getactivityname= request.POST['name']
                getactivitycategory= ActivityCategory.objects.filter(category_name=request.POST['activity_category'])[0]           
                getactivitydescription= request.POST['description']
                getjustification= request.POST['justification']
                getevidence= request.POST['evidence']
                ActivitySuggestion.objects.create(activity_name = getactivityname , category=getactivitycategory, activity_description=getactivitydescription, justification=getjustification,
                evidence_needed = getevidence , points = 1)
                return render(request,"activities/Suggest_activity.html", {
                    'categories': categories,
                    'suc_message': "Activity has been successfully submitted"
                })
            else:
                return render(request,"activities/Suggest_activity.html", {
                'categories': categories,
                'err_message': "Admin cannot submit a suggestion"
            })
        else:
            return render(request,"activities/Suggest_activity.html", {
            'categories': categories,       
            })
            

