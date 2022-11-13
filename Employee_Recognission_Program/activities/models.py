from email.policy import default
from types import NoneType
from wsgiref.validate import validator
from django.db import models
from Users.models import User, ROLE
from enum import Enum
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from Rewards.models import budget , budget_in_point
import datetime
from distutils.log import error


# Create your models here.
def validate_date_of_action(value):
    present = datetime.datetime.now()
    if not value.date() <= present.date():
        raise ValidationError(_("You can not submit date of action with a future date."))
    
def validate_year(value):
    today = datetime.datetime.now()

    year = today.year
    
    if not value.year == year:
        raise ValidationError(_("You can not submit date that exceeds current year."))

def validate_none(value):
    if value is None:
        raise ValidationError(_('Owner field cannot be null.'))

def validate_exist(value):
    if not User.objects.filter(pk = value).exists():
        raise ValidationError(_('Employee Doesn\'t exist'))
        
    

   
  


    
    
        
def validate_budget(value):
    if not budget_in_point.objects.filter(year = datetime.datetime.now().year).exists():
        raise ValidationError(_("Please add a budget before creating a Category"))
    else:
        total_budget = budget_in_point.objects.filter(year = datetime.datetime.now().year)[0].current_budget
        used_budget = ActivityCategory.objects.aggregate(Sum('threshhold'))['threshhold__sum']
        if(not used_budget):
            used_budget = 0
        if(value>total_budget):
            raise ValidationError(_("Budget exceeded the limit"))
       

    


class ActivityCategory(models.Model):
    category_name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    description =  models.CharField(max_length=255,null=False, blank= False, default="")
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateField(editable=True, null = False, blank = False, default = datetime.date.today(), validators = [validate_year])
    end_date = models.DateField(editable=True , null = False, blank = False ,  default = datetime.date(datetime.datetime.now().year, 12, 31), validators = [validate_year])
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank = False, related_name="category_owner",validators = [validate_exist,validate_none])
    budget = models.IntegerField(null = True, blank = True)
    threshhold = models.IntegerField(null = False, blank = False,  validators = [validate_budget])
    is_archived = models.BooleanField(null=False,blank = False , default=False)
    class Meta:
        verbose_name_plural = "Categories"

    def clean(self, *args, **kwargs):
        
        if self.start_date is None :
            raise ValidationError("Please enter required fields")
        
        elif(self.start_date >= self.end_date):
            raise ValidationError("Start Date must be before end date")
        if not ActivityCategory.objects.filter(pk = self.id).exists():
            if self.threshhold + ActivityCategory.objects.aggregate(Sum('threshhold'))['threshhold__sum'] > budget_in_point.objects.filter(year = datetime.datetime.now().year)[0].current_budget:
                
                raise ValidationError(_("Category threshhold exceeded the system budget"))
        else:
            if (ActivityCategory.objects.aggregate(Sum('threshhold'))['threshhold__sum'] - ActivityCategory.objects.filter(pk = self.id)[0].threshhold) + self.threshhold > budget_in_point.objects.filter(year = datetime.datetime.now().year)[0].current_budget:
                raise ValidationError(_("Category threshhold exceeded the system budget"))
        # if (self.start_date.month <= datetime.now().month and self.start_date.day < datetime.now().day):
        #     print(888)
        #     self.is_archived = True
        
                
                 
                
                
            
            
          

        # if self.owner is None:
        #     raise ValidationError(_("Owner field can't be empty"))
        if not self.threshhold == self.budget or self.budget is None:
            self.budget = self.threshhold
            
        

        super().clean(*args, **kwargs)
        
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.category_name}'






class Activity(models.Model):
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=True , blank = False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True , blank = True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateField(default = datetime.date.today(), validators = [validate_year])
    end_date = models.DateField(default = datetime.date(datetime.date.today().year, 12, 31) , null=True , validators = [validate_year])
    is_approved = models.BooleanField(null=False,blank = False , default=False)
    is_archived = models.BooleanField(null=False,blank = False , default=False)
    class Meta:
        verbose_name_plural = "Activities"

    def clean(self, *args, **kwargs):
        if(self.start_date >= self.end_date):
            raise ValidationError("Start Date must be before end date")
        if self.category is not None:            
            if self.points > self.category.threshhold:
                raise ValidationError(_("points cannot have a higher value than the category threshhold"))

        if self.category is None:
            raise ValidationError("must assign a category to the activity")
            
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
    is_archived = models.BooleanField(default = False)
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
    class Meta:
        verbose_name_plural = "Points"
    




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
 




