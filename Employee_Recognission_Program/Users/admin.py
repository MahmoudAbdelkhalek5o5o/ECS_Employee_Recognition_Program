from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from activities.models import Activity, ActivityCategory
from .models import User  , announcement , UserRegisterationRequest 
from .resources import UsersResource
from django.contrib import messages
from reversion.admin import VersionAdmin
from django.utils.translation import gettext_lazy as _

# from .forms import UserForm
# Register your models here.
class Filter(admin.SimpleListFilter):
    title = _('Active')
    parameter_name = 'is_active'
    # default = 'Yes'
    def lookups(self, request, model_admin):

        return (
            (None, _('Active')),
            
            ('yes', _('Archived')),

            ("all",_('all')),
        )



    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        
        if self.value() == 'yes':
            return queryset.filter(is_active = False)  

        elif self.value() == None:
            return queryset.filter(is_active = True)



@admin.action(description='Restore User')
def AdminRestoreUser (modeladmin, request, queryset):
    count=0
    for obj in queryset:
        cat = User.objects.filter(emp_id = obj.emp_id)[0]
        if cat.is_active == False:
            User.objects.filter(emp_id=cat.emp_id).update(is_active = True)
            count=count+1
        else:
            messages.error(request, f'User with id {cat.emp_id} and the name of {cat.first_name} {cat.last_name} cannot be restored since it already is not archived')  
    if count != 0:
            messages.success(request, f'{count} User(s) restored successfully')
def Archive(self, request, queryset):
    count = 0
    for obj in queryset:
        user = User.objects.filter(emp_id = obj.emp_id)[0]
        if user.is_active == True:
            User.objects.filter(emp_id=user.emp_id).update(is_active = False)
            count=count+1
            if ActivityCategory.objects.filter(owner = obj.emp_id).exists():
                ActivityCategory.objects.filter(owner = obj.emp_id).update(is_archived = True)
               


        else:
            messages.error(request, f'User {user.first_name} {user.last_name} cannot be archived since its already archived')  
    if count != 0:
            messages.success(request, f'{count} User(s) archived successfully')
    
    queryset.update(is_active = False)



@admin.register(User)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = UsersResource
    actions= [AdminRestoreUser,Archive]
    list_display = ['username' ,'emp_id' , 'first_name' , 'last_name' ,  'role']
    fields = ('first_name', 'last_name' ,'emp_id' ,  'username' , 'email' ,'phone_number','role', 'groups', 'user_permissions','is_staff','is_active')
    list_filter = (Filter,'role')
    search_fields =  ('username','first_name','last_name')
    resource_class = UsersResource
    


       
    # form = UserForm


admin.site.register(announcement)
admin.site.register(UserRegisterationRequest)



