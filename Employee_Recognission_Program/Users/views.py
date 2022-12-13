from django.forms import ValidationError
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
# from .resources import UsersResource
import pytz
from tablib import Dataset
from .resources import UsersResource
# from activities.models import ActivityCategory
from .models import  User , UserRegisterationRequest , ROLE
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, change_password_form, UpdateUserForm , UpdateUserrequestForm , SignupForm, Active_Form
from django import forms
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from tablib import Dataset
from activities.models import Points
from datetime import datetime
from .forms import UpdateUserForm
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    
    
    
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


def validate_domain(data):
    if '@' in data:
        domain = data.split('@')[1]
        ecsDomain = "ecs-co.com"
        if len(data.split('@')[0])<3:
            return False
        if domain == ecsDomain:
            return True
        return False
    return False

def validate_password(password):
        if (any(x.isupper() for x in password) and any(x.islower() for x in password) 
        and any(x.isdigit() for x in password)):
            return True
        return False

def get_error_messages_register(user):
    error_messages = {}
    if len(user['username'])<3 or len(user['username'])>20:
        error_messages['username']="Username length must be greater than 3 and less than 20"
    if len(user['first_name'])<3 or len(user['first_name'])>20:
        error_messages['first_name']="First name length must be greater than 3 and less than 20"
    if len(user['last_name'])<3 or len(user['last_name'])>20:
        error_messages['last_name']="Last name length must be greater than 3 and less than 20"
    if not validate_domain(user['email']):
        error_messages['email']="Please enter an Email Address with ecs domain"
    if not validate_password(user['password']) or len(user['password'])<8 or len(user['password'])>16:
        error_messages['password'] = "Password must contain digits, uppercase and lowercase letter with length between 8 and 16"
    if user["password"] != user["confirmation"]:
        error_messages['confirmation']="Passwords must match."
    if user['number_0'] == '':
        error_messages['number']="Country Code is required"
    if user['number_1'] == '':
        error_messages['number']="Phone number is required"
    if user['emp_id'] == '':
        error_messages['emp_id']="ID is required"
    # if not 'img' in user or user['img'] == '':
    #     error_messages.append("Profile Picture is required")
    return error_messages
# Create your views here.



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST,request.FILES)
        user = request.POST.dict()
        user.pop('csrfmiddlewaretoken')
        if 'img' in request.FILES:
            user["img"]=request.FILES["img"]
        else:
            user.pop('img')
        user['phone_number'] = user['number_0'] + " " + user["number_1"]
        # form constraints
        error_messages = get_error_messages_register(user)
        user.pop('number_0')
        user.pop('number_1')
        user.pop('confirmation')
        # phone number validation error
        if not form.is_valid():
            error_messages['number']="Enter a valid phone number (e.g. (20) 01000123456) or a number with an international call prefix."
        # form validation errors

        # username already exists
        if not 'username' in error_messages:
            if User.objects.filter(username=user["username"], is_active=False).exists():
                error_messages['username'] = "Username already exists"
        # ID already exists
        if not 'emp_id' in error_messages:
            if User.objects.filter(emp_id=user["emp_id"], is_active=False).exists() :
                error_messages['emp_id'] = "ID already exists"
        # email already exists
        if not 'email' in error_messages:
            if User.objects.filter(email=user["email"], is_active=False).exists() :
                error_messages['email'] = "Email already exists"
        # phone number already exists
        if not 'number' in error_messages:
            if User.objects.filter(phone_number=user["phone_number"], is_active=False).exists():
                error_messages['number'] = "Phone number already exists"
            
        if not error_messages == {}:
            print(error_messages)
            return render(request, "accounts/sign_up.html", {
                "error_messages": error_messages,
                'form':form,
            })
        # Attempt to create new user
        try:
            # database constraints errors
            UserRegisterationRequest.objects.create(**user)
            # user request created successfully
            send_mail(
                        'Registeration Request',
                        'Your registeration request has been successfully submitted. The admin will review your request shortly.',
                        'muhammad.mazen4@gmail.com.com',
                        [f'{user["email"]}'],
                        fail_silently=False,
                                            )
            return render(request, "accounts/sign_up.html", {
                "success_message": "Registeration request has been submitted and will be reviewed by HR soon",
                'form':RegisterForm()
                })
        except IntegrityError:
            # username already exists
            
            if UserRegisterationRequest.objects.filter(emp_id=request.POST["emp_id"], is_archived=False).exists():
                return render(request, "accounts/sign_up.html", {
                    "message": "Your request is pending",
                    'form':form,
                })
    else:
        return render(request, "accounts/sign_up.html", {'form':RegisterForm()
        })

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":

        # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            if User.objects.filter(username = username).exists():
                
                if User.objects.filter(username = username)[0].password is None:
                    return render(request, "accounts/login.html", {
                    "message": "Please activate your account by clicking on activate account."
                })
                
            
            user = authenticate(request, username=username, password=password)
        # Check if authentication successful
            if user is not None:
                login(request, user)
                if request.user.role == ROLE[0][0]:
                    return redirect("/admin")
                else:
                    return redirect("users-home")
        #if authentication is not succesful an error message is displayed
            else:
                return render(request, "accounts/login.html", {
                    "message": "Invalid username and/or password."
                })
        else:
            return render(request, "accounts/login.html")
    else:
         logout(request)
         return redirect('login')
    


    
def logout_view(request):
    logout(request)
    return redirect('login')



def userEdit(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST , request.FILES, instance=request.user)
            
            if user_form.is_valid():
              
                # if not user_form.validate_phone_number() and  request.user.phone_number == user_form.validate_phone_number():
                 
                #     return render(request, 'accounts/useredit_form.html', {
                #         'user_form': user_form,
                #         'message':'Phone number already exists'
                #     }
                #     )
                   
                if not user_form.clean_username():
                     return render(request, 'accounts/useredit_form.html', {
                        'user_form': user_form,
                           'message':'Username already exists'
                    }
                           )
                    
                    
                    
             
                else:   
                    user_form.save('user_form.is_valid()')
                
    
                    messages.success(request, 'Your profile is updated successfully')
                    return redirect(to='users-home')
            else:
                return render(request, 'accounts/useredit_form.html', {
                        'user_form': user_form,
                           'message':'Username or mobile already exists!'
                    }
                           )
        else:
            user_form = UpdateUserForm(instance=request.user)
       

        return render(request, 'accounts/useredit_form.html', {'user_form': user_form})
    else:
        return redirect("login")
    

def change_password(request):
    if request.user.is_authenticated:
        form = change_password_form()

        if request.method == 'POST':
            form = change_password_form(request.POST)
            if form.is_valid():
                password = request.POST["password"]
                user = authenticate(username=request.user.username, password=password) #authenticates if the old password entered is correct
                if user is not None:
                    if not form.validate_password():
                        return render(request,'accounts/change.html', {
                            'form': form,
                            'err_message':"Password must contains digits, uppercase and lowercase letter" # if confirmation and new password are not equivelant generate a message to enter passwords that match
                    })
                    new_password=request.POST["New_password"] #if old password is correct the user should enter the new password
                    confirmation = request.POST["confirmation"] #the user should confirm the new password entered and write it again
                    if new_password == confirmation:
                        create_password = make_password(new_password) # if the confirmed password entered is the same as the new password update the password
                        User.objects.filter(pk = request.user.emp_id).update(password = create_password)
                        #logout(request,request.user)
                        return redirect('login') #redirects the user to the login page to login with the new password
                    else:
                        return render(request,'accounts/change.html', {
                            'form': form,
                            'err_message':"passwords don't match" # if confirmation and new password are not equivelant generate a message to enter passwords that match
                        })

                else:
                
                    return render(request,'accounts/change.html', {
                        'form': form,
                        'message':"Old password is incorrect" #if old password is incorrect generate a message to tell the user to enter the correct old password

        })
        
  
        else:
            print(8)
            return render(request,'accounts/change.html', {
                    'form': form, 
                    
        })
    else:
        return redirect("login")

def points_about_expire(request):
    if not request.user.role == "Role.A":
        result = []
        points_categorized = []
        utc=pytz.UTC
        now = utc.localize(datetime.now())  
        points = Points.objects.filter(employee = request.user)
        expired_points = Points.objects.filter(employee=request.user,is_used = False)
        used_points=Points.objects.filter(employee=request.user, is_used=True)
      
        for point in expired_points:
            if now > point.end_date:
                 points_categorized.append(point)
        for point in points:
            delta = point.end_date - now
            if delta.days <= 30 and point.is_used == False and delta.days > 0:
                result.append(point)
        return render(request,"accounts/Points_view.html",{
            "points":result,
            "used_points":used_points,
            "expired_points": points_categorized,
        })
    else:
        return redirect("login")