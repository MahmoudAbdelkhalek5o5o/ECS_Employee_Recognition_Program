from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import Vendors , Rewards , Suggest_vendor , OldDataVendors , ArchivedVendors , OldDataRewards , ArchiveRewards , Redemption_Request , OldDataSuggest_Vendor , budget
from .resources import VendorResource , RewardResource

# Register your models here.



@admin.register(Vendors)
class ViewAdmin(ImportExportModelAdmin):
        resource_class = VendorResource



@admin.register(Rewards)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = RewardResource

admin.site.register(Suggest_vendor)
admin.site.register(OldDataVendors)
admin.site.register(ArchivedVendors)
admin.site.register(OldDataRewards)
admin.site.register(ArchiveRewards)
admin.site.register(Redemption_Request)
admin.site.register(OldDataSuggest_Vendor)
admin.site.register(budget)

