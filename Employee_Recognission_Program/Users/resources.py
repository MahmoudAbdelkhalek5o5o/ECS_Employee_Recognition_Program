from import_export import resources
from .models import User
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect

from django.core.exceptions import ValidationError


class UsersResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('id',)
        import_id_fields = ('emp_id',)
        fields = ['emp_id' , 'first_name' , 'last_name' , 'username' , 'email','role']
        
    def before_import(self, dataset, using_transactions, dry_run = False, **kwargs):
        for row in dataset:
                send_mail(
                    'Activity Request',
                    f'{User.username} Created an account at the Employee Recogmition Programfor you.',
                    'muhammad.mazen4@gmail.com',
                    [f'{row[3]}'],
                    fail_silently=False,)            
            
    