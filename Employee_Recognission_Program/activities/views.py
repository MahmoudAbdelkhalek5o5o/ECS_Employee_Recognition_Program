from django.shortcuts import render
from asyncio.windows_events import NULL
from contextlib import nullcontext
from pydoc import describe
from unicodedata import category
from urllib import request
from django.shortcuts import render, redirect
from datetime import datetime,date,timedelta
from django.core.mail import send_mail
from dateutil.relativedelta import relativedelta

from .models import  ActivityRequest, ActivityRequest, Activity, ActivityCategory ,Points,ActivitySuggestion , STATUS
from Users.models import User ,announcement , ROLE
from Rewards.models import budget , Suggest_vendor , budget_in_point
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
        
        if(request.method == 'GET'):
            
            return render(request,"activities/submit_activity_request.html",{
                "activity":activity
            })
        else:
            if activity.points - activity.category.threshhold > 0:
                Activity.objects.filter(pk = activity.id).update(is_archived = True)
                return render(request,"activities/submit_activity_request.html",{
                            "err_message":"you can't submit any request from this activity anymore.",
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
                            "err_message":"you can't submit activity request for category owner or admin",
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
            



def view_activity_requests(request):
    if request.user.is_authenticated:
        if request.user.role == ROLE[1][0] or request.user.role == ROLE[0][0]:
            categories = ActivityCategory.objects.filter(owner = request.user)
            activity_requests = ActivityRequest.objects.filter(category__in = categories , status = STATUS[0][0])
            return render(request,"activities/view_activity_requests.html",{
                "activity_requests": activity_requests
            })
        if request.user.role == ROLE[2][0]:
            activity_requests = ActivityRequest.objects.filter(employee = request.user)
            return render(request,"activities/view_activity_requests.html",{
                "activity_requests": activity_requests
            })
        
    else:
        return redirect("login")

def accept_activity_request(request,request_id):
    if request.user.is_authenticated:
        if request.user.role == ROLE[1][0]:
            activity_request = ActivityRequest.objects.filter(pk = request_id)[0]
            if activity_request.category.owner == request.user:
                ActivityRequest.objects.filter(pk = request_id).update(status = STATUS[1][0])
                budget_in_point.objects.filter(year = datetime.now().year).update(current_budget = budget_in_point.objects.filter(year = datetime.now().year)[0].current_budget - activity_request.activity.points)
                User.objects.filter(pk = activity_request.employee.emp_id).update(points = User.objects.filter(pk = activity_request.employee.emp_id)[0].points + activity_request.activity.points)
                budget.objects.update(budget = (budget_in_point.objects.filter(year = datetime.now().year)[0].current_budget * budget.objects.filter(year = datetime.now().year)[0].EGP)// budget.objects.filter(year = datetime.now().year)[0].point)
                Points.objects.create(points = activity_request.activity.points , employee = activity_request.employee , end_date = date.today() + relativedelta(months=+6), amounts = (activity_request.activity.points * budget.objects.filter(year = datetime.now().year)[0].EGP)//budget.objects.filter(year = datetime.now().year)[0].point)
                # send_mail(
                #     'Activity Request',
                #     'Your activity request has been accepted, the equivalent points have been added to your account and will expire in 6 months.',
                #     'muhammad.mazen4@gmail.com',
                #     [f'{activity_request.employee.email}'],
                #     fail_silently=False,
                #                         )
        return redirect("view_activity_requests")
    else:
        return redirect("login")
        
    
def decline_activity_request(request,request_id):
    if request.user.is_authenticated:
        if request.user.role == ROLE[1][0]:
            activity_request = ActivityRequest.objects.filter(pk = request_id).select_related('category')[0]
            if activity_request.category.owner == request.user:
                ActivityRequest.objects.filter(pk = request_id).update(status = STATUS[2][0])
                ActivityCategory.objects.filter(pk = activity_request.activity.category.id).update(threshhold = activity_request.activity.category.threshhold + activity_request.activity.points)
            # send_mail(
            #         'Activity Request',
            #         'Your activity request has been rejected.',
            #         'muhammad.mazen4@gmail.com',
            #         [f'{activity_request.employee.email}'],
            #         fail_silently=False,
            #                             )
       
        return redirect("view_activity_requests")
    else:
        return redirect("login")

def withdraw_activity_request(request,request_id):
    if request.user.is_authenticated:
        if request.user.role == ROLE[2][0]:
            activity_request = ActivityRequest.objects.filter(pk = request_id, employee_id = request.user.emp_id)[0]
            ActivityRequest.objects.filter(pk = request_id, employee_id = request.user.emp_id).update(status = STATUS[3][0])
            Activity.objects.filter(pk = activity_request.activity.id).update(points = activity_request.activity.category.threshhold + activity_request.activity.points)

        return redirect("view_activity_requests")
    else:
        return redirect("login")

def view_my_requests(request):
    if request.user.is_authenticated:
        activity_requests = ActivityRequest.objects.filter(employee = request.user)
        return render(request,"activities/owner_view_his_activity_requests.html",{
                "activity_requests": activity_requests
        })
    
    else:
        return redirect("login")