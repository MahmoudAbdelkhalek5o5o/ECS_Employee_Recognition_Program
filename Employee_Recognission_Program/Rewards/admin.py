from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import  Suggest_vendor , Redemption_Request  , budget , Vendor, Reward
from .resources import VendorResource , RewardResource

# Register your models here.

<<<<<<< Updated upstream

=======
@admin.action(description='Restore Vendor')
def AdminRestoreVendor (modeladmin, request, queryset):
    utc=pytz.UTC
    now = utc.localize(datetime.now())
    count=0
    for obj in queryset:
        cat = Vendor.objects.filter(id = obj.id)[0]
        if cat.end_date >= now and cat.is_archived==True:
            Vendor.objects.filter(id=cat.id).update(is_archived = False)
            count=count+1
        elif cat.is_archived==False:
            messages.error(request, f'Vendor with id {cat.id} and the name of {cat.name} cannot be restored since it already is not archived')  
        else:
            messages.error(request, f'Vendor with id {cat.id} and the name of {cat.name} cannot be restored after the end date.')  
    if count != 0:
        messages.success(request, f'{count} Vendor(s) restored 0')  

@admin.action(description='Restore Reward')
def AdminRestoreReward (modeladmin, request, queryset):
    utc=pytz.UTC
    now = utc.localize(datetime.now())
    count=0
    for obj in queryset:
        cat = Reward.objects.filter(id = obj.id)[0]
        if cat.end_date >= now and cat.vendor.is_archived==False and cat.is_archived==True:
            Reward.objects.filter(id=cat.id).update(is_archived = False)
            count=count+1
        elif cat.is_archived==False:
            messages.error(request, f'Reward with id {cat.id} cannot be restored since it already is not archived') 
        elif cat.category.is_archived==True:
            messages.error(request, f'Reward with id {cat.id} cannot be restored since the parent category with the name {cat.vendor.name} is archived')       
        else:
            messages.error(request, f'Reward with id {cat.id} cannot be restored after the end date.')  
    if count != 0:
        messages.success(request, f'{count} Reward(s) restored successfully')
>>>>>>> Stashed changes

@admin.register(Vendor)
class ViewAdmin(ImportExportModelAdmin):
        resource_class = VendorResource



@admin.register(Reward)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = RewardResource

admin.site.register(Suggest_vendor)

admin.site.register(Redemption_Request)
admin.site.register(budget)

