from email.policy import default
from django.db import models

# Create your models here.
from datetime import datetime
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from xmlrpc.client import DateTime
from django.db import models
from Users.models import User, Role
from django.core.exceptions import ValidationError



from enum import Enum

# Create your models here.
def validate_admin(value):
    employee = User.objects.get(pk = value)
    if employee.role == "Admin" or employee.role == "ADMIN" :
        raise ValidationError("You can't make a redemption request")
def validate_year(value):
    today = datetime.now()

    year = today.year
    
    if not value.year == year:
        raise ValidationError("You can not submit date that exceeds current year.")
    
def validate_year_forbudget(value):
    today = datetime.now()

    year = today.year
    
    if not value == int(year):
        raise ValidationError("You can not submit date that exceeds current year.")

class Vendor(models.Model):
    name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    vendor_policy = models.CharField(max_length=5000 , null = True)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True , null=False , validators = [validate_year])
    end_date = models.DateTimeField(editable = True , null = True , validators = [validate_year])
    img = models.ImageField(upload_to='images/', null = False , blank = True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = True, default = User , editable = False ,related_name="vendor_creator")
    accepts_voucher = models.BooleanField(null=False , default = False)
    accepts_procurement = models.BooleanField(null=False , default = False)
    accepts_direct = models.BooleanField(null=False , default = False)
    is_archived = models.BooleanField(default = False)
    def clean(self, *args, **kwargs):
        if(self.start_date>self.end_date):
            raise ValidationError("Start Date must be before end date")
    def __str__(self):
        return f"{self.id} {self.name}"




    
class Reward(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=False , blank = False)
    creation_day = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True , validators = [validate_year])
    end_date = models.DateTimeField(editable=True , validators = [validate_year])
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = True, related_name="reward_creator")
    points_equivalent = models.IntegerField(null = False, blank = False)
    is_archived = models.BooleanField(default = False)
    def clean(self, *args, **kwargs):
        if(self.start_date>self.end_date):
            raise ValidationError("Start Date must be before end date")


class Redemption_Request(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
    employee = models.ForeignKey(User , on_delete = models.CASCADE, null = True , related_name="employee" , validators = [validate_admin])
    voucher = models.ForeignKey(Reward,on_delete=models.CASCADE , null=False , blank=False)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS, default=STATUS[0][1])
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="admin")
    request_date = models.DateTimeField(auto_now_add=True,editable=False)
    approved_date = models.DateTimeField(null=True)
  


    
    
class Suggest_vendor(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
    vendor = models.CharField(max_length=30,null=False, blank= False, unique = False)
    website = models.CharField(max_length=255,null=False, blank= False, unique = False)
    reason = models.CharField(max_length=1024,null=False, blank= False, unique = False)
    is_archived = models.BooleanField(null=False , default = False)
    status = models.CharField(max_length=20, null = False , blank = False, choices=STATUS , default=STATUS[0])
    


    





    
    
class budget(models.Model):
    budget = models.IntegerField(null = False, blank = False)
    admin = models.ForeignKey(User, on_delete = models.CASCADE , null=True)
    point = models.IntegerField(null = True, blank = False)
    EGP = models.IntegerField(null = True, blank = False)
    budget_compare = models.IntegerField(null = False, blank = False)
    year = models.IntegerField(null = False , default= datetime.now().year , validators = [validate_year_forbudget])
    start_date = models.DateTimeField(auto_now_add=True)
    Archived_at = models.DateTimeField(null = True , blank = True, default = None)
    is_active = models.BooleanField(null=False , default=True)
    
    
 
    
    
        