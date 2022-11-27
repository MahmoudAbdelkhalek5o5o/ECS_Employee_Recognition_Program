from django.shortcuts import redirect, render
import pytz
from datetime import datetime,date,timedelta
from .models import Suggest_vendor ,Vendor , Reward 
from Users.models import User , ROLE
# Create your views here.
def suggest_vendor(request):
    if request.method== "POST":
        if not request.user.role == ROLE[0][0]:
            getvendorname= request.POST['vendor']
            getwebsite= request.POST['website']
            getreason= request.POST['reason']
            Suggest_vendor.objects.create(vendor = getvendorname , website=getwebsite, reason=getreason)
            
            return render(request,"rewards/suggest_vendor.html", {
                'suc_message': "Vendor suggestion has been successfully submitted"
            })
        else:
            return render(request,"rewards/suggest_vendor.html", {
                'err_message': "Admin cannot submit a suggestion"
            })
    else:
               
        return render(request,"rewards/suggest_vendor.html")

def view_vendors(request):
    if request.user.is_authenticated:
        all_vendors = Vendor.objects.filter().all()
        vendors = []
        utc=pytz.UTC
        now = utc.localize(datetime.now())
        for vendor in all_vendors:
            if vendor.start_date <= now:
                vendors.append(vendor)
        return render(request,"rewards/view_vendors.html",{
            "vendors": vendors
        })
    else:
        redirect("users-home")

def view_rewards(request,vendor_id):
    if request.user.is_authenticated:
        Reward.objects.filter(end_date__lt=date.today()).update(is_archived= True)
        rewards = Reward.objects.filter(is_archived = False, vendor = vendor_id)
        rewards1 = Reward.objects.filter(is_archived = False, vendor = vendor_id)[0]
        print(rewards1)
        return render(request,"rewards/view_rewards.html",{
            "rewards":rewards,
            "rewards1":rewards1
        })
    else:
        return redirect("users-home")