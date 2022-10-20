from django.contrib import admin
from django.contrib import messages

from import_export.admin import ImportExportModelAdmin
from .models import CategoryArchive , Activity ,ActivitySuggestion , ActivityCategory , ActivityArchive , ActivityRequest , ActivityRestorationRequest , OldActivityRequest , OldDataActivities , OldDataActivitySuggestion , OldDataCategory

from datetime import datetime
import pytz
# Register your models here.




@admin.action(description='Archive Activity')
def AdminArchiveCategory(modeladmin, request, queryset):
    queryset.update(is_archived = True)
    # messages.error(request, f'Activity cannot be restored after the end date of id {cat.id} with the name of {cat.activity_name}')  
    messages.success(request, f'Activity(ies) Archived successfully')  
    




# Register your models here.

@admin.register(ActivityCategory)
class ViewAdmin(ImportExportModelAdmin):
    actions = [AdminArchiveCategory]
    list_filter = ('is_archived','end_date')



@admin.register(Activity)
class ViewAdmin(ImportExportModelAdmin):
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

