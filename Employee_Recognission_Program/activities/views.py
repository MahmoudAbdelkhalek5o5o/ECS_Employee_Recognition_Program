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
            
            
def categories_view(request):
    if(request.user.is_authenticated):
        ActivityCategory.objects.filter(end_date__lt=date.today()).update(is_archived= True)
        categories = ActivityCategory.objects.filter(is_archived = False).select_related("owner")
        print(categories)
        return render(request,"activities/categories_view.html",{
            "categories":categories
        })
    else:
        return redirect("users-home")
    
def category_activities_view(request,category_id):
    if(request.user.is_authenticated):
        Activity.objects.filter(end_date__lt=date.today()).update(is_archived= True)
        activities = Activity.objects.filter(is_archived = False, category = ActivityCategory.objects.get(pk=category_id)).select_related("category")
        print(activities)
        return render(request,"activities/category_activities_view.html",{
            "activities":activities
        })
    else:
        return redirect("users-home")
    
def submit_activity_request(request, activity_id):
    if(request.user.is_authenticated):
        if(request.method == 'GET'):
            activity = Activity.objects.filter(pk=activity_id).select_related('category')[0]
            print(activity)
            return render(request,"activities/submit_activity_request.html",{
                "activity":activity
            })
        else:
            pass # submit activity request to be done
    else:
        return redirect("users-home")
            

