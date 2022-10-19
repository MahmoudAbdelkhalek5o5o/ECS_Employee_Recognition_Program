from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import CategoryArchive , Activity ,ActivitySuggestion , ActivityCategory , ActivityArchive , ActivityRequest , ActivityRestorationRequest , OldActivityRequest , OldDataActivities , OldDataActivitySuggestion , OldDataCategory
# Register your models here.

@admin.register(ActivityCategory)
class ViewAdmin(ImportExportModelAdmin):
        pass



@admin.register(Activity)
class ViewAdmin(ImportExportModelAdmin):
    pass

admin.site.register(ActivityArchive)
admin.site.register(CategoryArchive)
admin.site.register(ActivityRequest)
admin.site.register(ActivityRestorationRequest)
admin.site.register(OldActivityRequest)
admin.site.register(OldDataActivities)
admin.site.register(OldDataActivitySuggestion)
admin.site.register(OldDataCategory)
admin.site.register(ActivitySuggestion)

