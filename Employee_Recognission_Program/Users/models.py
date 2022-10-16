from email.policy import default
from msilib.schema import IniFile
from wsgiref.validate import validator
from django.contrib.auth.models import AbstractUser

from django.db import models
from enum import Enum
from PIL import Image
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
    role = models.CharField(max_length = 20 , choices = ROLE , null = False , default = ROLE[0][1])
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')
    points = models.IntegerField(default=0)

class OldDataUser(models.Model):
    ROLE = [
        ("ADMIN" , "Admin"),
        ("CATEGORYOWNER" , "CategoryOwner"),
        ("EMPLOYEE" , "Employee"),

              
    ]
    original_emp_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=20, null = False , blank = False)
    first_name = models.CharField(max_length=20, null = False , blank = False)
    last_name = models.CharField(max_length=20, null = False , blank = False)
    email = models.EmailField(null = False, blank = False , unique = True)
    img = models.ImageField(upload_to='images/', null = True , blank = True, default = 'images/plus.png')
    role = models.CharField(max_length = 20 , choices = ROLE , null = False)
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')
    points = models.IntegerField(default=0)
    edit_date = models.DateTimeField(editable=True,null=True)
    edit_by = models.ForeignKey(User , on_delete = models.CASCADE , null = False , related_name = "edited_by")

    
    

    
class announcements(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE,null=True )
    PostText= models.CharField(max_length=1024,null=False, blank= False)
    StartDate= models.DateTimeField(auto_now_add=True,editable=False)
    EndDate=models.DateTimeField(editable=False)
    is_archived = models.BooleanField(null=False , default = False)

class UserRegisterationRequests(models.Model):
    username = models.CharField(max_length=20, null = False , blank = False)
    first_name = models.CharField(max_length=20, null = False , blank = False)
    last_name = models.CharField(max_length=20, null = False , blank = False)
    password = models.CharField(max_length=100, null = False , blank = False, default='123456Abc')
    email = models.EmailField(null = False, blank = False)
    emp_id = models.IntegerField(null = False, blank = False , primary_key= True, unique = True)
    img = models.ImageField(upload_to='images/', null = True , blank = True, default = 'Logo.png')
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')


class OldDataUserRegisterationRequests(models.Model):
    ROLE = [
        ("ADMIN" , "Admin"),
        ("CATEGORYOWNER" , "CategoryOwner"),
        ("EMPLOYEE" , "Employee"),

              
    ]
    original_request = models.ForeignKey(UserRegisterationRequests,on_delete=models.CASCADE,null = False)
    username = models.CharField(max_length=20, null = False , blank = False)
    first_name = models.CharField(max_length=20, null = False , blank = False)
    last_name = models.CharField(max_length=20, null = False , blank = False)
    password = models.CharField(max_length=100, null = False , blank = False, default='123456Abc')
    email = models.EmailField(null = False, blank = False)
    emp_id = models.IntegerField(null = False, blank = False , primary_key= True, unique = True)
    img = models.ImageField(upload_to='images/', null = True , blank = True, default = 'Logo.png')
    role = models.CharField(max_length=20, null = False , blank = False, choices=ROLE)
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')
    edit_date = models.DateTimeField(auto_now_add=True , null=False)
    edit_by = models.ForeignKey(User , on_delete = models.CASCADE , null = False , related_name = "edited_registeration_by")


class RejectedUserRegisterationRequests(models.Model):
    request = models.ForeignKey(UserRegisterationRequests,on_delete=models.CASCADE,null=False )
    username = models.CharField(max_length=20, null = False , blank = False)
    first_name = models.CharField(max_length=20, null = False , blank = False)
    last_name = models.CharField(max_length=20, null = False , blank = False)
    email = models.EmailField(null = False, blank = False)
    emp_id = models.IntegerField(null = False, blank = False , primary_key= True, unique = True)
    img = models.ImageField(upload_to='images/', null = True , blank = True, default = 'Logo.png')
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')
    reject_date = models.DateTimeField(auto_now_add=True , null=False)
    rejected_by = models.ForeignKey(User , on_delete = models.CASCADE , null = False)
