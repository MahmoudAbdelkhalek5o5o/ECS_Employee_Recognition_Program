from django.http import HttpResponse
from django.shortcuts import render
from asyncio.windows_events import NULL
from contextlib import nullcontext
from pydoc import describe
from unicodedata import category
from urllib import request
from django.shortcuts import render, redirect
from datetime import datetime,date,timedelta
from django.core.mail import send_mail

from .models import ActivityArchive, ActivityEdit, ActivityCategoryEdit, ActivityRequest, ActivityRequest, Activity, ActivityCategory ,Points,ActivitySuggestion
from Users.models import User ,announcements
from Rewards.models import budget
import pytz
from django.forms.models import model_to_dict

# Create your views here.

def mine(request):
    categ = ActivityCategory(category_name = "Mezo",
    description = "adsfjo", start_date = None, end_date = None,
    owner = User.objects.get(pk = 3324), budget = 80001,
    budget_compare = 80001)
    errors = categ.clean()
    str = ""
    if (errors):
        for error in errors:
           str+= errors[error] + "\n"
    else:
        categ.save()
    #categ.delete()
    #ActivityCategory.objects.filter(category_name='hamed').delete()
    return HttpResponse(str)


def delete_activity(request,activity_id):
    if request.user.is_authenticated:
        if request.user.role == "Role.A":
            activity = Activity.objects.filter(pk = activity_id)
            # check if there is any edit requests before the admin delete the activity
            if (ActivityEdit.objects.filter(original_activity=activity)!=None):
                request.session['resp'] = "Check EDit requests" # set in session
                return redirect('activities:Category_view')# return same page with warning
            else:
                Activity.objects.filter(pk = activity_id).update(is_archived=True)
                # create copy in archive table of activity
                ActivityArchive.objects.create(activity_name=activity.activity_name,
                activity_description= activity.activity_description,
                category = activity.category,
                points= activity.points,
                approved_by = activity.approved_by,
                evidence_needed = activity.evidence_needed,
                creation_date = activity.creation_date,
                archived_by = activity.archived_by,
                start_date = activity.start_date,
                end_date = activity.end_date,
                is_approved = activity.is_approved,
                archive_date = activity.archive_date)

                return redirect("activities:Category_view")
        else:
            return redirect("users-home")
    else:
        return redirect('login')


def delete_category(request, category_id):
    if request.user.is_authenticated:
        if request.user.role == 'Role.A':
            category = ActivityCategory.objects.filter(pk=category_id)
            # check if there is any edit requests before the admin delete the activity
            if (ActivityCategoryEdit.objects.filter(original_category=category)!=None):
                request.session['resp'] = "Check EDit requests" # set in session
                return redirect('activities:Category_view') # return same page with warning
            else:
                Activity.objects.filter(pk = category_id).update(is_archived=True)
                # create copy in archive table of activity
                ActivityArchive.objects.create(activity_name=category.category_name,
                category_name= category.category_name,
                description = category.description,
                creation_date= category.creation_date,
                start_date = category.start_date,
                end_date = category.end_date,
                owner = category.owner,
                budget = category.budget,
                budget_compare = category.budget_compare,
                archive_date = category.archive_date,
                archived_by = category.archived_by
                )
                return redirect("activities:Category_view")
        else:
            return redirect("users-home")
    else:
        return redirect('login')