from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from activities.models import Activity, ActivityCategory
from .models import User  , announcement , UserRegisterationRequest  , ROLE
from .resources import UsersResource
from django.contrib import messages
from reversion.admin import VersionAdmin
from django.utils.translation import gettext_lazy as _
import datetime
from .forms import announcementForm
# from .forms import UserForm
# Register your models here.

@admin.action(description='Restore')
def AdminRestoreAnnouncement (modeladmin, request, queryset):
    for obj in queryset:
        if announcement.objects.filter(id = obj.id)[0].is_archived == True:

            announcement.objects.filter(id = obj.id).update(is_archived = False)
            
            messages.success(request, f'{announcement.objects.filter(id = obj.id)[0].title} announcement restored successfully')
        else:
            messages.error(request, f'{announcement.objects.filter(id = obj.id)[0].title} announcement not archived')


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


class Filter2(admin.SimpleListFilter):
    title = _('Active')
    parameter_name = 'is_archived'
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
            return queryset.filter(is_archived = True)  

        elif self.value() == None:
            return queryset.filter(is_archived = False)
        



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


from django.utils.html import format_html

@admin.register(User)
# class ImageAdmin(admin.ModelAdmin):

#     def image_tag(self, obj):
#         return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.img.url))

#     list_display = ['image_tag' , 'username' ,'emp_id' , 'first_name' , 'last_name' ,  'role']
class ViewAdmin(ImportExportModelAdmin , admin.ModelAdmin):
    

    resource_class = UsersResource
    actions= [AdminRestoreUser,Archive]
    list_display = ['username' ,'emp_id' , 'first_name' , 'last_name' ,  'role']
    fields = ('first_name', 'last_name' ,'emp_id' ,  'username' , 'email' ,'phone_number','role','img', 'groups', 'user_permissions','is_staff','is_active')
    list_filter = (Filter,'role')
    search_fields =  ('username','first_name','last_name')
    def get_queryset(self, request):
        data = super().get_queryset(request)
        to_archive = data.filter(role = ROLE[0][0], is_staff = False)
        to_archive.update(is_staff = True)
        for category in to_archive:
            Activity.objects.filter(category = category).update(is_archived = True)
            ActivityCategory.objects.filter(pk = category.id).update(is_archived = True)
        return data
        
    resource_class = UsersResource
    


       
    # form = UserForm
@admin.register(announcement)

class View_announcements(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'creator':
            return announcementForm(queryset=User.objects.filter(pk = request.user.emp_id))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_filter = [Filter2]
    list_display = ['creator','title', 'StartDate' , 'EndDate' , 'is_archived']
    search_fields = ['title','creator__username' , 'creator__first_name' , 'creator__last_name']
    fields = ('title', 'PostText' , 'StartDate' , 'EndDate' , 'is_archived')
    actions = [AdminRestoreAnnouncement]
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()

    def get_queryset(self, request):
        data = super().get_queryset(request)
        to_archive = data.filter(EndDate__lte=datetime.date.today())
        to_archive.update(is_archived=True)
        for ann in to_archive:
            announcement.objects.filter(pk = ann.id).update(is_archived = True)
          
        return data



    
admin.site.register(UserRegisterationRequest)



