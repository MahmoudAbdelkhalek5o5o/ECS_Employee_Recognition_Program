from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import Vendors
from .resources import VendorResource

# Register your models here.



@admin.register(Vendors)
class ViewAdmin(ImportExportModelAdmin):
    pass