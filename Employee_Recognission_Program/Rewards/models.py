from datetime import datetime
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from xmlrpc.client import DateTime
from django.db import models
from Users.models import User, Role


from enum import Enum

# Create your models here.


class Vendors(models.Model):
    name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    vendor_policy = models.CharField(max_length=5000 , null = True)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True , null=False)
    end_date = models.DateTimeField(editable = True , null = True)
    img = models.ImageField(upload_to='images/', null = False , blank = True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = True, related_name="vendor_creator")
    accepts_voucher = models.BooleanField(null=False , default = False)
    accepts_procurement = models.BooleanField(null=False , default = False)
    accepts_direct = models.BooleanField(null=False , default = False)

class OldDataVendors(models.Model):
    original_vendor = models.ForeignKey(Vendors,on_delete=models.CASCADE,null=False , blank = False)
    name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    vendor_policy = models.CharField(max_length=5000 , null = True)
    creation_date = models.DateTimeField(editable=False)
    start_date = models.DateTimeField(editable=True , null=False)
    end_date = models.DateTimeField(editable = True , null = True)
    img = models.ImageField(upload_to='images/', null = False , blank = True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = True)
    update_date = models.DateTimeField(auto_now_add = True , editable = True , null = True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="vendor_updater")
    accepts_voucher = models.BooleanField(null=False)
    accepts_procurement = models.BooleanField(null=False)
    accepts_direct = models.BooleanField(null=False)

class ArchivedVendors(models.Model):
    id = models.IntegerField(null = False, blank = False , primary_key = True)
    original_vendor = models.ForeignKey(Vendors,on_delete=models.CASCADE,null=False , blank = False)
    name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    vendor_policy = models.CharField(max_length=5000 , null = True)
    creation_date = models.DateTimeField(editable=False)
    start_date = models.DateTimeField(editable=True , null=False)
    end_date = models.DateTimeField(editable = True , null = True)
    img = models.ImageField(upload_to='images/', null = False , blank = True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = True)
    accepts_voucher = models.BooleanField(null=False)
    accepts_procurement = models.BooleanField(null=False)
    accepts_direct = models.BooleanField(null=False)
    update_date = models.DateTimeField(auto_now_add=True , editable = True , null = True)
    archived_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="vendor_archiver")
    




    
class Rewards(models.Model):
    vendor = models.ForeignKey(Vendors,on_delete=models.CASCADE,null=False , blank = False)
    creation_day = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = True, related_name="reward_creator")
    points_equivalent = models.IntegerField(null = False, blank = False)

class OldDataRewards(models.Model):
    original_voucher = models.ForeignKey(Rewards,on_delete=models.CASCADE,null=True)
    creation_day = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = True)
    points_equivalent = models.IntegerField(null = False, blank = False)
    update_date = models.DateTimeField(auto_now_add=True , editable = True , null = False)
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="reward_updater")

class ArchiveRewards(models.Model):
    id = models.IntegerField(null = False, blank = False , primary_key = True)
    creation_day = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = True)
    points_equivalent = models.IntegerField(null = False, blank = False)
    archived_date = models.DateTimeField(auto_now_add=True , editable = True , null = False)
    archived_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="archiver_reward")



    

    

class Redemption_Request(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
    employee = models.ForeignKey(User , on_delete = models.CASCADE, null = True , related_name="employee")
    voucher = models.ForeignKey(Rewards,on_delete=models.CASCADE , null=False , blank=False)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS, default=STATUS[0][1])
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="admin")
    request_date = models.DateTimeField(auto_now_add=True,editable=False)
    approved_date = models.DateTimeField(null=True)
    is_rejected = models.BooleanField(null=False , default = False)


    
    
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
    status = models.CharField(max_length=20, null = False , blank = False, choices=STATUS , default=STATUS[0][1])
    


    




class OldDataSuggest_Vendor(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
    original_suggestion= models.ForeignKey(Suggest_vendor , on_delete = models.CASCADE, null = True)
    vendor = models.CharField(max_length=30,null=False, blank= False, unique = False)
    website = models.CharField(max_length=255,null=False, blank= False, unique = False)
    reason = models.CharField(max_length=1024,null=False, blank= False, unique = False)
    edit_delete_date = models.DateTimeField(editable=True,null=True)
    edited = models.BooleanField(null=False,blank = False, default=False)
    deleted = models.BooleanField(null=False,blank = False, default=False)
    update_date = models.DateTimeField(auto_now_add=True , editable = True , null = False)
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="vendorsuggestion_updater")
    status = models.CharField(max_length=20, null = False , blank = False, choices=STATUS , default=STATUS[0][1])


    
    
    
class budget(models.Model):
    budget = models.IntegerField(null = False, blank = False)
    admin = models.ForeignKey(User, on_delete = models.CASCADE , null=True)
    point = models.IntegerField(null = True, blank = False)
    EGP = models.IntegerField(null = True, blank = False)
    budget_compare = models.IntegerField(null = False, blank = False)
    year = models.IntegerField(null = False , default= datetime.now().year)
    start_date = models.DateTimeField(auto_now_add=True)
    Archived_at = models.DateTimeField(null = True)
    is_active = models.BooleanField(null=False , default=True)
    
    
 
    
    
        