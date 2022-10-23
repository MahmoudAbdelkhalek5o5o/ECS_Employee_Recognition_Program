from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import User  , announcement , UserRegisterationRequest 
from .resources import UsersResource
from django.contrib import messages
# from .forms import UserForm
# Register your models here.

<<<<<<< Updated upstream
=======
@admin.action(description='Restore User')
def AdminRestoreUser (modeladmin, request, queryset):
    count=0
    for obj in queryset:
        cat = User.objects.filter(emp_id = obj.emp_id)[0]
        if cat.is_archived==True:
            User.objects.filter(emp_id=cat.emp_id).update(is_archived = False)
            count=count+1
        else:
            messages.error(request, f'User with id {cat.emp_id} and the name of {cat.first_name} {cat.last_name} cannot be restored since it already is not archived')  
    if count != 0:
            messages.success(request, f'{count} User(s) restored successfully')

>>>>>>> Stashed changes
@admin.register(User)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = UsersResource
    actions= [AdminRestoreUser]
    list_filter = ('is_archived',)
    # form = UserForm
    
admin.site.register(announcement)
admin.site.register(UserRegisterationRequest)



