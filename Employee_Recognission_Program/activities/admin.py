from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
<<<<<<< Updated upstream
from .models import CategoryArchive , Activity ,ActivitySuggestion , ActivityCategory , ActivityArchive , ActivityRequest , ActivityRestorationRequest , OldActivityRequest , OldDataActivities , OldDataActivitySuggestion , OldDataCategory
=======
from numpy import rec
from .models import CategoryArchive , Activity ,ActivitySuggestion , ActivityCategory  , ActivityRequest  
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


>>>>>>> Stashed changes
# Register your models here.

@admin.register(ActivityCategory)
class ViewAdmin(ImportExportModelAdmin):
        pass



@admin.register(Activity)
class ViewAdmin(ImportExportModelAdmin):
<<<<<<< Updated upstream
    pass

admin.site.register(ActivityArchive)
=======
    actions = [AdminRestoreActivity]
    list_filter = ('is_archived',)
>>>>>>> Stashed changes
admin.site.register(CategoryArchive)
admin.site.register(ActivityRequest)
admin.site.register(ActivitySuggestion)

