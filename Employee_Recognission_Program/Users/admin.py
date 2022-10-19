from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import User , OldDataUser , announcements , UserRegisterationRequests , OldDataUserRegisterationRequests , RejectedUserRegisterationRequests
from .resources import UsersResource
from .forms import UserForm
# Register your models here.



@admin.register(User)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = UsersResource
    form = UserForm
    
admin.site.register(OldDataUser)
admin.site.register(announcements)
admin.site.register(UserRegisterationRequests)
admin.site.register(OldDataUserRegisterationRequests)
admin.site.register(RejectedUserRegisterationRequests)


