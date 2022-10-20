from django.contrib import admin
from django.contrib import messages

from activities.models import ActivityCategory, Activity, ActivityRequest


from datetime import datetime
import pytz
# Register your models here.




@admin.action(description='Archive Activity')
def AdminArchiveCategory(modeladmin, request, queryset):
    count=0
    queryset.update(is_archived = True)
    # Activity.objects.create(id=cat.id,activity_name=cat.activity_name,activity_description=cat.activity_description,category=cat.category,start_date=cat.start_date,
    # end_date=cat.end_date,points=cat.points,approved_by=cat.approved_by,evidence_needed=cat.evidence_needed,creation_date=cat.creation_date,is_approved=cat.is_approved)
    # obj.delete()
    # count=count+1
    # messages.error(request, f'Activity cannot be restored after the end date of id {cat.id} with the name of {cat.activity_name}')  
    if count != 0:
        messages.success(request, f'{count} Activity(ies) restored successfully')  
class ArchiveCategory(admin.ModelAdmin):
    actions = [AdminArchiveCategory]


admin.site.register(ActivityCategory,ArchiveCategory)
admin.site.register(Activity)
admin.site.register(ActivityRequest)