from email.policy import default
from wsgiref.validate import validator
from django.db import models
from Users.models import User, Role
from enum import Enum
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from Rewards.models import budget
from datetime import datetime

# Create your models here.
def validate_date_of_action(value):
    present = datetime.now()
    if not value.date() <= present.date():
        raise ValidationError("You can not submit date of action with a future date.")
    
def validate_year(value):
    today = datetime.now()

    year = today.year
    
    if not value.year == year:
        raise ValidationError("You can not submit date that exceeds current year.")

        

    
    
        
def validate_budget(value):
    total_budget = budget.objects.filter(Archived_at = None)[0].budget_compare
    used_budget = ActivityCategory.objects.aggregate(Sum('budget_compare'))['budget_compare__sum']
    if(not used_budget):
        used_budget = 0
    if(value>total_budget-used_budget):
        raise ValidationError("Budget exceeded the limit")

class ActivityCategory(models.Model):
    category_name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    description =  models.CharField(max_length=255,null=False, blank= False, default="")
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True, null = True, blank = True, validators = [validate_year])
    end_date = models.DateTimeField(editable=True , null = True, blank = True ,  validators = [validate_year])
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="category_owner")
    budget = models.IntegerField(null = False, blank = False, validators = [validate_budget])
    budget_compare = models.IntegerField(null = False, blank = False)
    is_archived = models.BooleanField(null=False,blank = False , default=False)

    def clean(self, *args, **kwargs):
        if(self.start_date>self.end_date):
            raise ValidationError("Start Date must be before end date")
        if(self.budget_compare<self.budget):
            raise ValidationError("Remaining budget can not be bigger than the original budget")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.category_name






class Activity(models.Model):
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True , validators = [validate_year])
    end_date = models.DateTimeField(editable=True,null=True , validators = [validate_year])
    is_approved = models.BooleanField(null=False,blank = False , default=False)
    is_archived = models.BooleanField(null=False,blank = False , default=False)

    def clean(self, *args, **kwargs):
        if(self.start_date>self.end_date):
            raise ValidationError("Start Date must be before end date")
        category_budget = self.category.budget
        conversion_rate = budget.objects.filter(Archived_at = None)[0].EGP / budget.objects.filter(Archived_at = None)[0].point
        if(self.points*conversion_rate>category_budget):
            raise ValidationError("Activity points cannot fit within the category remaining budget")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.activity_name







class ActivityRequest(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
    emp = models.ForeignKey(User, on_delete = models.CASCADE, null=True,related_name = "original_uploader")
    submission_date = models.DateTimeField(auto_now_add=True)
    date_of_action = models.DateTimeField(null = False , validators = [validate_date_of_action])
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,  null=False, db_constraint= True)
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE,  null=True, db_constraint= True)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS, default=STATUS[0])
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, related_name="approver_of_upload")
    evidence_needed = models.CharField(max_length=1024,null=False, blank= False, default="Provide evidence please")
    proof_of_action = models.FileField(upload_to = "proofs/",null=False, blank= False)
    activity_approval_date = models.DateTimeField(auto_now_add=False, auto_now=False, null = True, blank = False)
    def clean(self, *args, **kwargs):
        if(self.emp == self.category.owner or self.emp.role == "Admin"):
            raise ValidationError("You can't make an activity request")
       


    
    
class ActivitySuggestion(models.Model):
    activity_name = models.CharField(max_length=30 , null = False, blank=False)
    category = models.ForeignKey(ActivityCategory , on_delete=models.CASCADE , null=False)
    activity_description = models.CharField(max_length=1024 , null = False, blank=False)
    justification = models.CharField(max_length=30 , null = True, blank=True)
    evidence_needed = models.CharField(max_length=1024 , null = True, blank=True)
    is_archived = models.BooleanField(null=False , default = False)
    
class Points(models.Model):
    points = models.IntegerField(null = False, blank = False)
    amounts = models.IntegerField(null = False, blank = False)
    start_date = models.DateTimeField(auto_now_add=True,editable=False)
    end_date = models.DateTimeField(editable=False)
    employee = models.ForeignKey(User , on_delete=models.CASCADE,null=True , related_name="earned_to")
    is_used = models.BooleanField(null=False,blank = False , default=False)
    




class ActivityRestorationRequest(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
    id = models.IntegerField(null = False, blank = False , primary_key = True)
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    archived_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="archived_activity_by")
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True,null=True)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS, default=STATUS[0])
 




