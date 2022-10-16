from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import User

# Register your models here.



@admin.register(User)
class ViewAdmin(ImportExportModelAdmin):
    pass