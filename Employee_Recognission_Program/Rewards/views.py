from django.shortcuts import render
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