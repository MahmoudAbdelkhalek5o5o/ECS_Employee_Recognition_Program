
from django.contrib.auth.models import AbstractUser

from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from audit_log.models.fields import LastUserField
from django.contrib.auth.models import Group
from django.utils import timezone
Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))


ROLE = [
        ("ADMIN" , "Admin"),
        ("CATEGORYOWNER" , "CategoryOwner"),
        ("EMPLOYEE" , "Employee"),

              
    ]
     
def validate_domain(data):
    if '@' in data:
        domain = data.split('@')[1]
        ecsDomain = "ecs-co.com"
        
        if domain != ecsDomain:
           
            raise ValidationError(
                _('Please enter an ecs domain. ex: example@ecs-co.com'),
                params={'value': data},
                )
    else:
        raise ValidationError(
                _('Please enter an ecs domain. ex: example@ecs-co.com'),
                params={'value': data},
                )
        

def validate_year(value):
    today = datetime.now()

    year = today.year
    
    if not value.year == year:
        raise ValidationError("You can not submit date that exceeds current year.")

# Create your models here.
class User(AbstractUser):
    
    email = models.EmailField(null = False, blank = False , unique = True , validators = [validate_domain])
    emp_id = models.IntegerField(null = False, blank = False , primary_key= True, unique = True,default=3324)
    img = models.ImageField(upload_to='images/', null = True , blank = True, default = 'images/plus.png')
    role = models.CharField(max_length = 20 , choices = ROLE , null = False ,blank = False, default = ROLE[0][0])
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')
    points = models.IntegerField(default=0)
    password = models.CharField(max_length=128, verbose_name='password' , blank = False , null = True)
    
    def clean(self, *args, **kwargs):
        
        if self.role == ROLE[0][0]:
            self.is_staff = True
        
        if User.objects.filter(username = self.username).exists():
            raise ValidationError('username already exists')
        super().clean(*args, **kwargs)
    
    

    
class announcement(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE,null=True )
    title = models.CharField(max_length=1024,null=False, blank= False)
  
    PostText= models.CharField(max_length=1024,null=False, blank= False)
    StartDate= models.DateTimeField(editable=True,default = timezone.now)
    EndDate=models.DateTimeField(editable=True,default = datetime(datetime.today().year, 12, 31))
    is_archived = models.BooleanField(null=False , default = False)
    def clean(self, *args, **kwargs):
        if(self.StartDate>self.EndDate):
            raise ValidationError("Start Date must be before end date")
    
    def __str__(self):
        return f"{self.id} {self.title}"

class UserRegisterationRequest(models.Model):
    username = models.CharField(max_length=20, null = False , blank = False)
    first_name = models.CharField(max_length=20, null = False , blank = False)
    last_name = models.CharField(max_length=20, null = False , blank = False)
    password = models.CharField(max_length=100, null = False , blank = False, default='123456Abc' , editable = False)
    email = models.EmailField(null = False, blank = False)
    emp_id = models.IntegerField(null = False, blank = False , primary_key= True, unique = True)
    img = models.ImageField(upload_to='images/', null = True , blank = True, default = 'Logo.png')
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')
    accept_user = models.BooleanField(default = False)
    def clean(self, *args, **kwargs):
        if self.accept_user == True:
            User.objects.create(emp_id = self.emp_id , username = self.username , first_name = self.first_name , 
            last_name = self.last_name , password = self.password , email = self.email , 
            phone_number = self.phone_number , role = ROLE[2][0] , img = self.img)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}'s request"


