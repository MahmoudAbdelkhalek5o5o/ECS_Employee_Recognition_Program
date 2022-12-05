from import_export import resources
from .models import User , ROLE
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
        
    def before_import(self, dataset, using_transactions, dry_run = True, **kwargs):
        for row in dataset:
            if row[5] == ROLE[0][0]:
                User.objects.filter(pk = row[4]).update(is_staff = True)
            if '@' in row[3]:
                domain = row[3].split('@')[1]
                ecsDomain = "ecs-co.com"
            if len(row[3].split('@')[0])<3:
                return False
            if domain != ecsDomain:
           
                raise ValidationError(
                    'Please enter an ecs domain. ex: example@ecs-co.com',
                    params={'value': row[3]},
                    )
            send_mail(
                    'Activity Request',
                    f'{User.username} Created an account at the Employee Recogmition Programfor you.',
                    'muhammad.mazen4@gmail.com',
                    [f'{row[3]}'],
                    fail_silently=False,)            
            
    