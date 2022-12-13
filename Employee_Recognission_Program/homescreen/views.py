from django.shortcuts import render
import datetime
from dateutil import parser
from django.shortcuts import render,redirect
from Users.models import announcement , ROLE , User , UserRegisterationRequest
from activities.models import ActivityCategory , Activity , ActivityRequest , ActivitySuggestion ,Points

from Rewards.models import budget , Vendor , Reward , Redemption_Request , Suggest_vendor
from django import forms
import pytz
from django_summernote.widgets import SummernoteWidget
from .import helpers
from datetime import date
from django.db.models import Q
# Create your views here.
from datetime import datetime
from threading import Timer
import schedule
import time




def expired():
    announcementss = announcement.objects.filter(is_archived = False).order_by("-StartDate")
    for Announcement in announcementss:
        if helpers.check_date(Announcement.EndDate) == False:
            announcement.objects.filter(EndDate = Announcement.StartDate).update(is_archived = True)
    categoriess = ActivityCategory.objects.filter(is_archived = False)
    for category in categoriess:
        if helpers.check_date(category.end_date) == True:
            ActivityCategory.objects.filter(start_date = category.start_date).update(is_archived = True)
       
    Activitiess = Activity.objects.filter(is_archived = False)
    for activity in Activitiess:
        if helpers.check_date(activity.start_date) == False or helpers.check_date(activity.end_date) == True:
            Activity.objects.filter(start_date = activity.start_date).update(is_archived = True)
    
    vendors = Vendor.objects.filter(is_archived = False)   
    for vendor in vendors:
        if helpers.check_date(vendor.start_date) == False or helpers.check_date(vendor.end_date) == True:
            Vendor.objects.filter(start_date = vendor.start_date).update(is_archived = True)
    
    rewards = Reward.objects.filter(is_archived = False)   
    for reward in rewards:
        if helpers.check_date(reward.start_date) == False or helpers.check_date(reward.end_date) == True:
            Reward.objects.filter(start_date = reward.start_date).update(is_archived = True)
schedule.every().day.at("10:30").do(expired)

def index(request):
    
   
        
    if request.user.is_authenticated:
        
        

        
        announcements = announcement.objects.filter(is_archived = False, StartDate__lte = datetime.today()).order_by("-StartDate")
     
        vendors = Vendor.objects.filter(is_archived = False)[:6]
        vendorsodd = []
        vendorseven = []
        
        i = 0
        for vendor in vendors:
            if i % 2 == 0:
                vendorseven.append(vendor)
                i+=1
            else:
                vendorsodd.append(vendor)
                i+=1
        if request.user.role == ROLE[1][0]:
            if not ActivityCategory.objects.filter(owner = request.user , is_archived = False):
                User.objects.filter(pk = request.user.emp_id).update(role = ROLE[2][0])
        if budget.objects.filter(year = datetime.now().year):
            Budget = budget.objects.filter(year = datetime.now().year)[0]
            rate = request.user.points * Budget.EGP // Budget.point
            return render(request , "homescreen/index.html" , {
            "vendorseven": vendorseven,
            "vendorsodd": vendorsodd,
            "vendors": vendors,
            "announcements":announcements,
            "rate":rate
        })
        else:
            return render(request , "homescreen/index.html" , {
            "vendorseven": vendorseven,
            "vendorsodd": vendorsodd,
            "vendors": vendors,
            "announcements":announcements
            })
    else:
        return redirect("login")


def Leaderboard(request):
    if request.user.is_authenticated:
        # first_place=User.objects.filter(~Q(role=ROLE[0][0] , is_active = True)).order_by("-points")[:1][0]
        # second_place=User.objects.filter(~Q(role=ROLE[0][0]  , is_active = True)).order_by("-points")[1:2][0]
        # third_place=User.objects.filter(~Q(role=ROLE[0][0]  , is_active = True)).order_by("-points")[2:3][0]
        # last_7=User.objects.filter(~Q(role=ROLE[0][0]  , is_active = True)).order_by("-points")[3:10]
        top10=User.objects.filter(~Q(role=ROLE[0][0]  , is_active = True)).order_by("-points")[:10]
        return render (request, "homescreen/leaderboard.html",{
            "top10":top10,
            # "first_place":first_place,
            # "second_place":second_place,
            # "third_place":third_place,
            # "last_7":last_7
        })
    
    else:
        return redirect("login")