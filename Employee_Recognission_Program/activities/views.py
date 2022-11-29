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
from . import helpers
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
        categoriess = ActivityCategory.objects.filter(is_archived = False)
        for category in categoriess:
            if helpers.check_date(category.end_date) == True:
                ActivityCategory.objects.filter(start_date = category.start_date).update(is_archived = True)
       
        Activitiess = Activity.objects.filter(is_archived = False)
        for activity in Activitiess:
            if helpers.check_date(activity.start_date) == False or helpers.check_date(activity.end_date) == True:
                Activity.objects.filter(start_date = activity.start_date).update(is_archived = True)
        
            
    

        
        categories = ActivityCategory.objects.filter(is_archived = False , start_date__lte = datetime.now())
        print(categories)
        return render(request,"activities/categories_view.html",{
            "categories":categories
        })
    else:
        return redirect("users-home")
    
def category_activities_view(request,category_id):
    activitiess = Activity.objects.filter(is_archived = False, category = ActivityCategory.objects.get(pk=category_id))
    for activity in activitiess:
        if activity.points - activity.category.threshhold > 0:
            Activity.objects.filter(pk = activity.id).update(is_archived = True)
        
    if(request.user.is_authenticated):
        activities = Activity.objects.filter(is_archived = False, category = ActivityCategory.objects.get(pk=category_id) , start_date__lte = datetime.now())
        return render(request,"activities/category_activities_view.html",{
            "activities":activities
        })
    else:
        return redirect("users-home")
    
def submit_activity_request(request, activity_id):
    
    if(request.user.is_authenticated):
        
        activity = Activity.objects.filter(pk=activity_id).select_related('category')[0]
        if activity.points - activity.category.threshhold > 0:
            Activity.objects.filter(pk = activity.id).update(is_archived = True)
        if(request.method == 'GET'):
            
            return render(request,"activities/submit_activity_request.html",{
                "activity":activity
            })
        else:
            if activity.is_archived == True:
                return render(request,"activities/submit_activity_request.html",{
                            "activity":activity,
                            "err_message":"you can't submit a request for this category anymore.",
                        })
            if datetime.strptime(request.POST["date"],'%Y-%m-%d')  > datetime.now():
                return render(request,"activities/submit_activity_request.html",{
                            "activity":activity,
                            "err_message":"you cant submit a request with a future date.",
                        })
                
            if request.user.role == ROLE[0][0] and not request.POST["submitted_to"]:
                 return render(request,"activities/submit_activity_request.html",{
                "activity":activity,
                "err_message":"Admin can't submit activity requests.",
            })
            
            elif request.POST["submitted_to"]:
                # checks if user exists
                if User.objects.filter(pk = request.POST["submitted_to"]).exists():
                    #checks if user is not admin nor the category owner
                    if not User.objects.filter(pk = request.POST["submitted_to"])[0].role == ROLE[0][0] and not int(request.POST["submitted_to"]) == activity.category.owner.emp_id:
                        # creates the activity request 
                        ActivityRequest.objects.create(employee = User.objects.filter(pk = request.POST["submitted_to"])[0]
                                                    , date_of_action = request.POST["date"], proof_of_action = request.FILES["proof"] , 
                                                    activity = activity ,category = activity.category , submitter = request.user)
                        # update the category threshhold 
                        ActivityCategory.objects.filter(activity = activity.id).update(threshhold = ActivityCategory.objects.filter(activity = activity.id)[0].threshhold - activity.points)

                        return render(request,"activities/submit_activity_request.html",{
                            "activity":activity,
                            "suc_message":"Activity request successfully submitted.",
                        })
                    else:
                        return render(request,"activities/submit_activity_request.html",{
                            "activity":activity,
                            "err_message":"you can't submit activity request for category owner",
                        })
                else:
                    return render(request,"activities/submit_activity_request.html",{
                            "activity":activity,
                            "err_message":"Employee Doesn't exist.",
                        })
            else:
                  # creates the activity request 
                ActivityRequest.objects.create(employee = request.user
                                               , date_of_action = request.POST["date"], proof_of_action = request.FILES["proof"] , 
                                                activity = activity ,category = activity.category , submitter = request.user)
                        # update the category threshhold 
                ActivityCategory.objects.filter(activity = activity.id).update(threshhold = ActivityCategory.objects.filter(activity = activity.id)[0].threshhold - activity.points)

                return render(request,"activities/submit_activity_request.html",{
                    "activity":activity,
                    "suc_message":"Activity request successfully submitted.",
                })
                      
                
    else:
        return redirect("users-home")
            

