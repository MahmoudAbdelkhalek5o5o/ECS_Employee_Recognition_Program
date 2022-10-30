from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import SimpleListFilter
from import_export.admin import ImportExportModelAdmin
from numpy import rec
from django.contrib.admin.models import LogEntry, CHANGE
from auditlog.registry import auditlog

from .models import  Activity ,ActivitySuggestion , ActivityCategory  , ActivityRequest , ActivityRestorationRequest  
from Users.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import pytz
# Register your models here.

class Filter(admin.SimpleListFilter):
    title = _('Archived')
    parameter_name = 'is_archived'
    # default = 'Yes'
    def lookups(self, request, model_admin):

        return (
            ("all",_('all')),
            ('yes', _('Archived')),
            (None, _('Not Archived')),
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
            return queryset.filter(is_archived=True)  

        elif self.value() == None:
            return queryset.filter(is_archived = False)




@admin.action(description='Archive Category')
def AdminArchiveCategory(modeladmin, request, queryset):
    for obj in queryset:
        LogEntry.objects.log_action(
            user_id=request.user.emp_id, 
            content_type_id= obj.id,
            object_id=obj.pk,
            object_repr=obj.description,
            action_flag=CHANGE,
            change_message="You have ...")
    queryset.update(is_archived = True)
    
    for category in queryset:
        Activity.objects.filter(category = category).update(is_archived = True)
        ActivityCategory.objects.filter(pk = category.id).update(is_archived = True)
        print (not ActivityCategory.objects.filter(owner = category.owner , is_archived = False).exists())
        if not ActivityCategory.objects.filter(owner = category.owner , is_archived = False).exists() and ( User.objects.filter(pk = category.owner.emp_id)[0].role == "CategoryOwner" or   User.objects.filter(pk = category.owner.emp_id)[0].role == "CATEGORYOWNER"):
            User.objects.filter(pk = category.owner.emp_id).update(role = "Employee")
        # ActivityRequest.objects.filter(category = category).update(is_archived = True)
    # messages.error(request, f'Activity cannot be restored after the end date of id {cat.id} with the name of {cat.activity_name}')  
    messages.success(request, f'Activity(ies) Archived successfully')  
    

@admin.action(description='Restore Category')
def AdminRestoreCategory (modeladmin, request, queryset):
    utc=pytz.UTC
    now = utc.localize(datetime.now())
    count=0
    for obj in queryset:
        cat = ActivityCategory.objects.filter(id = obj.id)[0]
        if cat.end_date >= now and cat.is_archived==True:
            ActivityCategory.objects.filter(id=cat.id).update(is_archived = False)
            count=count+1
        elif cat.is_archived==False:
            messages.error(request, f'Category with id {cat.id} and the name of {cat.category_name} cannot be restored since it already is not archived')  
        else:
            messages.error(request, f'Category with id {cat.id} and the name of {cat.category_name} cannot be restored after the end date.')  
        if obj.owner.role == "Employee" or obj.owner.role == "EMPLOYEE":
            User.objects.filter(pk = obj.owner.emp_id).update(role = "CategoryOwner")
    if count != 0:
            messages.success(request, f'{count} Category(ies) restored successfully')
        
       
@admin.action(description='Restore Activity')
def AdminRestoreActivity (modeladmin, request, queryset):
    utc=pytz.UTC
    now = utc.localize(datetime.now())
    count=0
    for obj in queryset:
        cat = Activity.objects.filter(id = obj.id)[0]
        if cat.end_date >= now and cat.category.is_archived==False and cat.is_archived==True:
            Activity.objects.filter(id=cat.id).update(is_archived = False)
            count=count+1
        elif cat.is_archived==False:
            messages.error(request, f'Activity with id {cat.id} and the name of {cat.activity_name} cannot be restored since it already is not archived') 
        elif cat.category.is_archived==True:
            messages.error(request, f'Activity with id {cat.id} and the name of {cat.activity_name} cannot be restored since the parent category with the name {cat.category.category_name} is archived')       
        else:
            messages.error(request, f'Activity with id {cat.id} and the name of {cat.activity_name} cannot be restored after the end date.')  
    if count != 0:
        messages.success(request, f'{count} Activity(ies) restored successfully')


# Register your models here.

@admin.register(ActivityCategory)
class ViewAdminCategory(ImportExportModelAdmin):
    actions = [AdminArchiveCategory, AdminRestoreCategory]
    fields = ('category_name', 'description','owner','start_date','end_date','total_budget','budget','is_archived')
    list_display = ["category_name","description","owner","start_date","end_date","is_archived"]
    list_filter = [Filter,"owner","start_date","end_date"]
    search_fields = ["category_name"]
    readonly_fields = ['budget']


    def get_queryset(self, request):
        data = super().get_queryset(request)
        to_archive = data.filter(end_date__lte=datetime.now())
        to_archive.update(is_archived=True)
        for category in to_archive:
            Activity.objects.filter(category = category).update(is_archived = True)
            ActivityCategory.objects.filter(pk = category.id).update(is_archived = True)
        return data


@admin.register(Activity)
class ViewAdmin(ImportExportModelAdmin):
    actions = [AdminRestoreActivity]
    list_filter = ('is_archived',)



admin.site.register(ActivityRequest)
admin.site.register(ActivityRestorationRequest)
admin.site.register(ActivitySuggestion)