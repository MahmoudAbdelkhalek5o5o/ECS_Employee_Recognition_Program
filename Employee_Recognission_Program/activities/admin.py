from django.contrib import admin

from activities.models import ActivityCategory, Activity

# Register your models here.
admin.site.register(ActivityCategory)
admin.site.register(Activity)