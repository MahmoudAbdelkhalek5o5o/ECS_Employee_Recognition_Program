from django.shortcuts import render , redirect
from .models import Suggest_vendor ,Vendor , Reward  ,Redemption_Request
from activities.models import Points
from Users.models import User , ROLE
from django.http import HttpResponseRedirect 
from django.urls import reverse
from datetime import datetime
import pytz
from django.contrib import messages

def is_expired(end_date):
    utc=pytz.UTC
    now = utc.localize(datetime.now())
    if now >= end_date:
        return True
    else:
        return False
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
        Reward.objects.filter(end_date__lt=datetime.now()).update(is_archived= True)
        rewards = Reward.objects.filter(is_archived = False, vendor = vendor_id)
        
        vendors = Vendor.objects.filter(is_archived = False, pk = vendor_id)[0]
        print(vendors)
        return render(request,"rewards/view_rewards.html",{
            "rewards":rewards,
            "rewards1":vendors
        })
    else:
        return redirect("users-home")
    
    
def redemption_request(request,voucher_id):
    if not request.user.role == ROLE[0][0]:
        voucher = Reward.objects.get(pk = voucher_id)
        if request.method == "POST":
            points_equivalent = voucher.points_equivalent
            if request.user.points >= voucher.points_equivalent:
                points_needed = []
                points = Points.objects.filter(employee = request.user,is_used = False).order_by('end_date')
                for point in points:
                    if is_expired(point.end_date) == False:
                        points_needed.append(point)
                for point in points_needed:
                    acquired = 0
                    if acquired < points_equivalent:
                        acquired = acquired + point.points
                        if acquired > points_equivalent:
                        
                            Points.objects.filter(pk = point.id).update(points = acquired - points_equivalent)
                            break
                        else:
                            Points.objects.filter(pk = point.id).update(is_used = True)
               
                User.objects.filter(username = request.user.username).update(points = request.user.points - points_equivalent)       
                Redemption_Request.objects.create(voucher = voucher,employee = request.user)
                messages.success(request, 'Redemption request successfully submitted.')
                return HttpResponseRedirect(reverse("view_rewards", args = (voucher.vendor.id,)))
            else:
                 messages.error(request, "you don't have enough points to redeem that reward.")
                 return HttpResponseRedirect(reverse("view_rewards", args = (voucher.vendor.id,)))
        
def redeem_procurement(request , vendor_id):
    if request.user.role == ROLE[0][0]:
        messages.error(request, "Admin can't make redemption request")
        return HttpResponseRedirect(reverse("view_rewards", args = (vendor_id,)))
    else:
        if int(request.POST["amount"]) <= request.user.points:
            print(int(request.POST["amount"]))
            reward = Reward.objects.create(vendor = Vendor.objects.get(pk = vendor_id) , creator = request.user , points_equivalent = int(request.POST["amount"]) , is_archived = True)
            points_equivalent = reward.points_equivalent
            if request.user.points >= reward.points_equivalent:
                points_needed = []
                points = Points.objects.filter(employee = request.user,is_used = False).order_by('end_date')
                for point in points:
                    if is_expired(point.end_date) == False:
                        points_needed.append(point)
                for point in points_needed:
                    acquired = 0
                    if acquired < points_equivalent:
                        acquired = acquired + point.points
                        if acquired > points_equivalent:
                        
                            Points.objects.filter(pk = point.id).update(points = acquired - points_equivalent)
                            break
                        else:
                            Points.objects.filter(pk = point.id).update(is_used = True)
               
                User.objects.filter(username = request.user.username).update(points = request.user.points - points_equivalent)       
                Redemption_Request.objects.create(voucher = reward,employee = request.user)
                messages.success(request, 'Redemption request successfully submitted.')
                return HttpResponseRedirect(reverse("view_rewards", args = (vendor_id,)))
            else:
                 messages.error(request, "you don't have enough points to redeem that reward.")
                 return HttpResponseRedirect(reverse("view_rewards", args = (vendor_id,)))
        
        else:
            messages.error(request, "you don't have enough points to redeem that reward.")
            return HttpResponseRedirect(reverse("view_rewards", args = (vendor_id,)))