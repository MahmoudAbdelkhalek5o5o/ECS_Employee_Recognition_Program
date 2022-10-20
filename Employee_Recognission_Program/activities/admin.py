from django.contrib import admin
from django.contrib import messages

from import_export.admin import ImportExportModelAdmin
from numpy import rec
from .models import CategoryArchive , Activity ,ActivitySuggestion , ActivityCategory , ActivityArchive , ActivityRequest , ActivityRestorationRequest , OldActivityRequest , OldDataActivities , OldDataActivitySuggestion , OldDataCategory
from django.utils.translation import gettext_lazy as _
from datetime import datetime
# Register your models here.

class Filter(admin.SimpleListFilter):
    title = _('Archived')
    parameter_name = 'Is Archived'
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
    # messages.error(request, f'Activity cannot be restored after the end date of id {cat.id} with the name of {cat.activity_name}')  
    messages.success(request, f'Activity(ies) Archived successfully')  
    




# Register your models here.

@admin.register(ActivityCategory)
class ViewAdminCategory(ImportExportModelAdmin):
    actions = [AdminArchiveCategory]
    list_filter = (Filter,)
    def get_queryset(self, request):
        data = super().get_queryset(request)
        data.filter(end_date__lte=datetime.now()).update(is_archived=True)
        return data.filter()


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

