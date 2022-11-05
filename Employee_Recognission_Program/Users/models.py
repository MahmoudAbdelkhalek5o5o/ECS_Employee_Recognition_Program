from email.policy import default
from msilib.schema import IniFile
from wsgiref.validate import validator
from django.contrib.auth.models import AbstractUser

from django.db import models
from enum import Enum
from PIL import Image
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from audit_log.models.managers import AuditLog
# from audit_log.models.fields import LastUserField
from auditlog.registry import auditlog
from django.contrib.auth.hashers import make_password


class Role(Enum):
     A = "Admin"
     M = "Manager"
     E = "Employee"
     
def validate_domain(data):
    if '@' in data:
        domain = data.split('@')[1]
        ecsDomain = "ecs-co.com"
        if len(data.split('@')[0])<3:
            return False
        if domain != ecsDomain:
           
            raise ValidationError(
                _('Please enter an ecs domain. ex: example@ecs-co.com'),
                params={'value': data},
                )
    return False

def validate_year(value):
    today = datetime.now()

    year = today.year
    
    if not value.year == year:
        raise ValidationError("You can not submit date that exceeds current year.")

# Create your models here.
class User(AbstractUser):
    ROLE = [
        ("ADMIN" , "Admin"),
        ("CATEGORYOWNER" , "CategoryOwner"),
        ("EMPLOYEE" , "Employee"),

              
    ]
    email = models.EmailField(null = False, blank = False , unique = True , validators = [validate_domain])
    emp_id = models.IntegerField(null = False, blank = False , primary_key= True, unique = True,default=3324)
    img = models.ImageField(upload_to='images/', null = True , blank = True, default = 'images/plus.png')
    role = models.CharField(max_length = 20 , choices = ROLE , null = False ,blank = False, default = ROLE[0][0])
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')
    points = models.IntegerField(default=0)
    def clean(self, *args, **kwargs):
        if self.password is not None :
            self.password = make_password(self.password)
        if self.role == 'ADMIN' or self.role == 'Admin':
            self.is_staff = True
        super().clean(*args, **kwargs)
    
    

    
class announcement(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE,null=True,editable = False )
    PostText= models.CharField(max_length=1024,null=False, blank= False)
    StartDate= models.DateTimeField(editable=True,default = datetime.now())
    EndDate=models.DateTimeField(editable=True,default = datetime(datetime.today().year, 12, 31))
    is_archived = models.BooleanField(null=False , default = False)
    def clean(self, *args, **kwargs):
        if(self.StartDate>self.EndDate):
            raise ValidationError("Start Date must be before end date")

class UserRegisterationRequest(models.Model):
    username = models.CharField(max_length=20, null = False , blank = False)
    first_name = models.CharField(max_length=20, null = False , blank = False)
    last_name = models.CharField(max_length=20, null = False , blank = False)
    password = models.CharField(max_length=100, null = False , blank = False, default='123456Abc')
    email = models.EmailField(null = False, blank = False)
    emp_id = models.IntegerField(null = False, blank = False , primary_key= True, unique = True)
    img = models.ImageField(upload_to='images/', null = True , blank = True, default = 'Logo.png')
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')


