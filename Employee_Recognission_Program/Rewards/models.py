from email.policy import default
from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _

from datetime import datetime
from django.db import models
from Users.models import User, ROLE
from django.core.exceptions import ValidationError
import pytz
from django.core.mail import send_mail


from enum import Enum
STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
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
def validate_ratio(value):
    if value <= 0:
        raise ValidationError(_("EGP and Point values can't be 0 or less"))

class Vendor(models.Model):
    name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    vendor_policy = models.CharField(max_length=5000 , null = True)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True , null=False , default = datetime.now() ,validators = [validate_year])
    end_date = models.DateTimeField(editable = True , null = True ,default = datetime(datetime.today().year, 12, 31), validators = [validate_year])
    img = models.ImageField(upload_to='images/', null = False , blank = True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = True  ,related_name="vendor_creator" )
    accepts_voucher = models.BooleanField(null=False , default = False)
    accepts_procurement = models.BooleanField(null=False , default = False)
    is_archived = models.BooleanField(default = False)
    def clean(self, *args, **kwargs):
        utc=pytz.UTC

        if(self.start_date>self.end_date):
            raise ValidationError("Start Date must be before end date")

        if self.start_date >= utc.localize(datetime.now()):
            self.is_archived = True
            
        
    def __str__(self):
        return f"{self.id} {self.name}"




    
class Reward(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=False , blank = False)
    creation_day = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True , default = datetime.now() ,validators = [validate_year])
    end_date = models.DateTimeField(editable=True , default = datetime(datetime.today().year, 12, 31),validators = [validate_year])
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = True, related_name="reward_creator" , editable= False)
    points_equivalent = models.IntegerField(null = False, blank = False)
    is_archived = models.BooleanField(default = False)
   

    def clean(self, *args, **kwargs):
        
        if(self.start_date>self.end_date):
            raise ValidationError(_("Start Date must be before end date"))
        if self.is_archived == False and self.vendor.accepts_voucher == False:
            Vendor.objects.filter(pk = self.vendor.id).update(accepts_voucher = True)
        
    def __str__(self):
        return f"{self.points_equivalent} Points from {self.vendor.name}"

class Redemption_Request(models.Model):
    
    employee = models.ForeignKey(User , on_delete = models.CASCADE, null = True , related_name="employee" , validators = [validate_admin] ,editable = False)
    voucher = models.ForeignKey(Reward,on_delete=models.CASCADE , null=False , blank=False)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS, default=STATUS[1][0])
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="admin" , editable = False)
    request_date = models.DateTimeField(auto_now_add=True,editable=False )
    approved_date = models.DateTimeField(null=True,default = datetime.now() , editable=False)
    
    def clean(self, *args, **kwargs):
        if self.status == STATUS[1][0]:
            self.approved_date = datetime.now()
        elif self.status == STATUS[3][0]:
            raise ValidationError(_("You can't withdraw a request you didn't make."))
        elif self.status == STATUS[2][0]:
            self.approved_date = datetime.now()
            User.objects.filter(pk = self.employee.emp_id).update(points = self.employee.points - self.voucher.points_equivalent)
            send_mail(
                    'Redemption Request',
                    'Admin has rejected your redemption request and the equivlent points were returned to your acoount.',
                    'muhammad.mazen4@gmail.com',
                    [f'{self.employee.email}'],
                    fail_silently=False,
                                        )
            
    def __str__(self):
        return f"{self.employee}'s redemption request"
    
    class Meta:
        verbose_name_plural = "redemption request" 


    
    
class Suggest_vendor(models.Model):
    
    vendor = models.CharField(max_length=30,null=False, blank= False, unique = False)
    website = models.CharField(max_length=255,null=False, blank= False, unique = False)
    reason = models.CharField(max_length=1024,null=False, blank= False, unique = False)
    is_archived = models.BooleanField(null=False , default = False)
    


    
    class Meta:
        
        verbose_name_plural = "Vendor suggestions"




    
    
class budget(models.Model):
    budget = models.IntegerField(null = False, blank = False)
    admin = models.ForeignKey(User, on_delete = models.CASCADE , null=True)
    point = models.IntegerField(null = False, blank = False , validators = [validate_ratio])
    EGP = models.IntegerField(null = False, blank = False , validators=[validate_ratio])
    budget_compare = models.IntegerField(null = True, blank = False)
    year = models.IntegerField(null = False , default= datetime.now().year , validators = [validate_year_forbudget])
    start_date = models.DateTimeField(auto_now_add=True)
    Archived_at = models.DateTimeField(null = True , blank = True, default = None)
    is_active = models.BooleanField(null=False , default=True)
    
    def clean(self, *args, **kwargs):
        if self.EGP <=0 or self.point <= 0:
            raise ValidationError(_("EGP and point values can't be Zero or less"))
        if self.budget_compare is None:
            self.budget_compare = self.budget
            budget_in_point.objects.create(current_budget = (self.budget * self.point)//self.EGP , total_budget = (self.budget * self.point)//self.EGP)

        
        if budget.objects.filter(year = datetime.now().year).exists():
            if self.budget +  budget.objects.filter(year = datetime.now().year)[0].budget >= 0:
                self.budget += budget.objects.filter(year = datetime.now().year)[0].budget
                self.budget_compare = self.budget
                if budget_in_point.objects.filter(year = datetime.now().year).exists():
                    budget_in_point.objects.filter(year = datetime.now().year).update(current_budget = (self.budget * self.point)//self.EGP , total_budget = (self.budget * self.point)//self.EGP)

            else:
                raise ValidationError(_('budget can\'t be less than 0'))
                
        elif self.budget < 0:
            raise ValidationError(_('budget can\'t be less than 0')) 
        

        
        super().clean(*args, **kwargs)

    def __str__(self):
        return f'{self.year} , {self.budget}EGP'
    
    
class budget_in_point(models.Model):
    current_budget = models.IntegerField(null = False, blank = False)
    total_budget = models.IntegerField(null = True, blank = False)
    year = models.IntegerField(null = False , default= datetime.now().year , validators = [validate_year_forbudget])
    start_date = models.DateTimeField(auto_now_add=True)
    def clean(self, *args, **kwargs):
        
        if not budget.objects.filter(year = datetime.now().year).exists():
            raise ValidationError("Must enter a budget before adding points.")
        else:
            Budget = budget.objects.filter(year = datetime.now().year)[0]
            if self.current_budget +  budget_in_point.objects.filter(year = datetime.now().year)[0].current_budget >= 0:
                    self.current_budget += budget_in_point.objects.filter(year = datetime.now().year)[0].current_budget
                    self.total_budget = self.current_budget 
                    budget.objects.filter(year = datetime.now().year).update(budget = (self.current_budget * Budget.EGP)//Budget.point)
            else:
                raise ValidationError(_('budget can\'t be less than 0'))
                
        super().clean(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Budget in points"
        
    def __str__(self):
        return f"{self.current_budget}"