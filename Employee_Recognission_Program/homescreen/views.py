from django.shortcuts import render
import datetime
from dateutil import parser
from django.shortcuts import render,redirect
from Users.models import announcement , ROLE , User , UserRegisterationRequest
# from activities.models import ActivityCategory , Activity , ActivityRequest , ActivitySuggestion ,Points

from Rewards.models import budget , Vendor , Reward , Redemption_Request , Suggest_vendor
from django import forms
import pytz
from django_summernote.widgets import SummernoteWidget
from .import helpers
from datetime import date
# Create your views here.

def index(request):
    
        
    if request.user.is_authenticated:
        announcements = announcement.objects.filter(is_archived = False).order_by("-StartDate")
        archived_announcements = announcement.objects.filter(is_archived = True).order_by("-StartDate")
        for Announcement in announcements:
            if helpers.check_date(Announcement.StartDate) == False:
                announcement.objects.filter(StartDate = Announcement.StartDate).update(is_archived = True)
        for Announcement in archived_announcements:
            if helpers.check_date(Announcement.StartDate) == True:
                announcement.objects.filter(StartDate = Announcement.StartDate).update(is_archived = False)

 
        vendors = Vendor.objects.filter(is_archived = False)[:6]
        vendorsodd = []
        vendorseven = []
        
        i = 0
        for vendor in vendors:
            if i % 2 == 0:
                vendorseven.append(vendor)
                i+=1
                print(vendorseven[0].img)
            else:
                vendorsodd.append(vendor)
                i+=1

                
        return render(request , "homescreen/index.html" , {
            "vendorseven": vendorseven,
            "vendorsodd": vendorsodd,
            "vendors": vendors,
            "announcements":announcements
        })
    else:
        return redirect("login")
