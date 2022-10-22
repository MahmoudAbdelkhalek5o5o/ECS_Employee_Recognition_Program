from django.contrib import admin
from django.contrib import messages

from import_export.admin import ImportExportModelAdmin
from numpy import rec
from .models import CategoryArchive , Activity ,ActivitySuggestion , ActivityCategory , ActivityArchive , ActivityRequest , ActivityRestorationRequest , OldActivityRequest , OldDataActivities , OldDataActivitySuggestion , OldDataCategory
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import pytz
# Register your models here.

class Filter(admin.SimpleListFilter):
    title = _('Archived')
    parameter_name = 'Is Archived'
    default = 'Yes'
    def lookups(self, request, model_admin):

        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(
                is_archived = True
            )
        if self.value() == 'No':
            return queryset.filter(
                is_archived = False
            )


@admin.action(description='Archive Category')
def AdminArchiveCategory(modeladmin, request, queryset):
    queryset.update(is_archived = True)
    for category in queryset:
        Activity.objects.filter(category = category).update(is_archived = True)
        ActivityRequest.objects.filter(category = category).update(is_archived = True)
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
    list_filter = (Filter,)
    def get_queryset(self, request):
        data = super().get_queryset(request)
        to_archive = data.filter(end_date__lte=datetime.now())
        to_archive.update(is_archived=True)
        for category in to_archive:
            Activity.objects.filter(category = category).update(is_archived = True)
            ActivityRequest.objects.filter(category = category).update(is_archived = True)
        return data


@admin.register(Activity)
class ViewAdmin(ImportExportModelAdmin):
    actions = [AdminRestoreActivity]
    list_filter = ('is_archived',)


admin.site.register(ActivityArchive)
admin.site.register(CategoryArchive)
admin.site.register(ActivityRequest)
admin.site.register(ActivityRestorationRequest)
admin.site.register(OldActivityRequest)
admin.site.register(OldDataActivities)
admin.site.register(OldDataActivitySuggestion)
admin.site.register(OldDataCategory)
admin.site.register(ActivitySuggestion)

