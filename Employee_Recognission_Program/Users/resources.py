from import_export import resources
from .models import User , ROLE
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.core.mail import get_connection, EmailMultiAlternatives

from django.core.exceptions import ValidationError


class UsersResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('id',)
        import_id_fields = ('emp_id',)
        fields = ['emp_id' , 'first_name' , 'last_name' , 'username' , 'email','role']
        
    def before_import(self, dataset, using_transactions, dry_run = True, **kwargs):
        for row in dataset.dict:
            if row["role"] == ROLE[0][0]:
                User.objects.filter(pk = row["emp_id"]).update(is_staff = True)
            if '@' in row["email"]:
                domain = row["email"].split('@')[1]
                ecsDomain = "ecs-co.com"
            if len(row["email"].split('@')[0])<3:
                return False
            if domain != ecsDomain:
           
                raise ValidationError(
                    'Please enter an ecs domain. ex: example@ecs-co.com',
                    params={'value': row["email"]},
                    )

            # connection = get_connection() # uses SMTP server specified in settings.py
            # connection.open() # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()

            # html_content = render_to_string('newsletter.html', {'newsletter': n,})               
            # text_content = f"{request.user} Created an account at the Employee Loyalty Program for you."                      
            # msg = EmailMultiAlternatives("subject", text_content, "muhammad.mazen4@gmail.com", ["to@bla", "to2@bla", "to3@bla"], connection=connection)                                      
            # msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
            # msg.send() 

            # connection.close() # Cleanup
            #             send_mail(
            #                     'Activity Request',
            #                     f'{User.username} Created an account at the Employee Recogmition Programfor you.',
            #                     'muhammad.mazen4@gmail.com',
            #                     [f'{row[3]}'],
            #                     fail_silently=False,)            
                        
                