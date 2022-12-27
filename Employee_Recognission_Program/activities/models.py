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
from django.core.mail import send_mail
from dateutil.relativedelta import relativedelta
from django.utils import timezone


# Create your models here.
STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
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
    
    
def validate_threshhold(value):
    if value <= 0:
        raise ValidationError(_("Category threshhold cannot be 0 or less."))
    

   
def validate_negative(value):
    if value <= 0:
        raise ValidationError(_("Points value can't be zero or less"))


    
    
        
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
    start_date = models.DateField(editable=True, null = False, blank = False, default = timezone.now, validators = [validate_year])
    end_date = models.DateField(editable=True , null = False, blank = False ,  default = datetime.date(datetime.datetime.now().year, 12, 31), validators = [validate_year])
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank = False, related_name="category_owner",validators = [validate_exist,validate_none])
    budget = models.IntegerField(null = True, blank = True)
    threshhold = models.IntegerField(null = False, blank = False,  validators = [validate_budget , validate_threshhold])
    is_archived = models.BooleanField(null=False,blank = False , default=False)
    class Meta:
        verbose_name_plural = "Categories"

    def clean(self, *args, **kwargs):
        if self.is_archived == True:
            Activity.objects.filter(category = self.id).update(is_archived = True)
        if self.owner.role == ROLE[2][0]:
            User.objects.filter(pk = self.owner.emp_id).update(role = ROLE[1][0])
        
        if self.start_date is None :
            raise ValidationError("Please enter required fields")
        
        elif(self.start_date >= self.end_date):
            raise ValidationError("Start Date must be before end date")
       
                
                 
                
                
            
            
          

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
    points = models.IntegerField(null = False, blank = False , validators=[validate_negative], default = 0)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True , blank = True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateField(default =timezone.now, validators = [validate_year])
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
    
    employee = models.ForeignKey(User, on_delete = models.CASCADE, null=True,related_name = "original_uploader",  editable=False)
    submitter = models.ForeignKey(User, on_delete = models.CASCADE, null=True,related_name = "submitter" ,  editable=False)
    submission_date = models.DateTimeField(auto_now_add=True)
    date_of_action = models.DateTimeField(null = False , validators = [validate_date_of_action],  editable=False)
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,  null=False, db_constraint= True ,  editable=False)
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE,  null=True, db_constraint= True,  editable=False)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS, default=STATUS[0][0])
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, related_name="approver_of_upload",  editable=False)
    evidence_needed = models.CharField(max_length=1024,null=False, blank= False, default="Provide evidence please")
    proof_of_action = models.FileField(upload_to = "proofs/",null=False, blank= False,  editable=False)
    activity_approval_date = models.DateTimeField(auto_now_add=False, auto_now=False, null = True, blank = False, editable=False)
    def clean(self, *args, **kwargs):
        
        if self.status == STATUS[3][0]:
            raise ValidationError(_("You can't withdraw a request you didn't make."))
        if self.category is None:
            raise ValidationError("must assign a category to the activity")
        if(self.employee == self.category.owner or self.employee.role == ROLE[0][0]):
            raise ValidationError("You can't make an activity request")
        
        if self.status == STATUS[1][0]:
            budget_in_point.objects.filter(year = datetime.datetime.now().year).update(current_budget = budget_in_point.objects.filter(year = datetime.datetime.now().year)[0].current_budget - self.activity.points)
            User.objects.filter(pk = self.employee.emp_id).update(points = User.objects.filter(pk = self.employee.emp_id)[0].points + self.activity.points)
            budget.objects.update(budget = (budget_in_point.objects.filter(year = datetime.datetime.now().year)[0].current_budget * budget.objects.filter(year = datetime.datetime.now().year)[0].EGP)// budget.objects.filter(year = datetime.datetime.now().year)[0].point)
            Points.objects.create(points = self.activity.points , employee = self.employee , end_date = datetime.datetime.now() + relativedelta(months=+6), amounts = (self.activity.points * budget.objects.filter(year = datetime.datetime.now().year)[0].EGP)//budget.objects.filter(year = datetime.datetime.now().year)[0].point)

            send_mail(
                    'Activity Request',
                    'Your activity request has been accepted, the equivalent points have been added to your account and will expire in 6 months.',
                    'muhammad.mazen4@gmail.com',
                    [f'{self.employee.email}'],
                    fail_silently=False,
                                        )
        elif self.status == STATUS[2][0]:
            Activity.objects.filter(pk = self.activity.id).update(points = self.activity.category.threshhold + self.activity.points)
            send_mail(
                    'Activity Request',
                    'Your activity request has been rejected.',
                    'muhammad.mazen4@gmail.com',
                    [f'{self.employee.email}'],
                    fail_silently=False,
                                        )
       
    def __str__(self):
        return f"{self.employee}'s request"

    
    
class ActivitySuggestion(models.Model):
    activity_name = models.CharField(max_length=30 , null = False, blank=False)
    category = models.ForeignKey(ActivityCategory , on_delete=models.CASCADE , null=False , editable = False)
    activity_description = models.CharField(max_length=1024 , null = False, blank=False)
    justification = models.CharField(max_length=30 , null = True, blank=True)
    evidence_needed = models.CharField(max_length=1024 , null = True, blank=True)
    points = models.IntegerField(null = False, blank = False)
    start_date = models.DateField(default =timezone.now, validators = [validate_year])
    end_date = models.DateField(default = datetime.date(datetime.date.today().year, 12, 31) , null=True , validators = [validate_year])
    is_accepted = models.BooleanField(null=False , default = False)
    
    def clean(self, *args, **kwargs):
        if self.is_accepted == True and not self.points is None:
            Activity.objects.create(activity_name = self.activity_name , activity_description = self.activity_description , category = self.category ,  evidence_needed = self.evidence_needed , points = self.points , start_date = self.start_date , end_date = self.end_date)
    def __str__(self):
        return f"{self.activity_name}"
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
 




