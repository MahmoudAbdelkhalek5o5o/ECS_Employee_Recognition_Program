from datetime import datetime
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import  Suggest_vendor , Redemption_Request  , budget , Vendor, Reward , budget_in_point ,STATUS
from .resources import VendorResource , RewardResource
import pytz
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django import forms

from django.contrib import messages

class redemptionForm(forms.ModelChoiceField):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            return redemptionForm(queryset=Redemption_Request.objects.filter(status=STATUS[0][0]))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
# Register your models here.
class Filter(admin.SimpleListFilter):
    title = _('Archived')
    parameter_name = 'is_archived'
    # default = 'Yes'
    def lookups(self, request, model_admin):

        return (
            (None, _('Active')),
            
            ('yes', _('Archived')),

            ("all",_('all')),
        )



    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        
        if self.value() == 'yes':
            return queryset.filter(is_archived=True)  

        elif self.value() == None:
            return queryset.filter(is_archived = False)

class Filter2(admin.SimpleListFilter):
    title = _('Accepted')
    parameter_name = 'is_accepted'
    # default = 'Yes'
    def lookups(self, request, model_admin):

        return (
            ("no", _('Accepted')),
            
            ('yes', _('not accepted')),

            (None,_('all')),
        )



    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        
        if self.value() == 'yes':
            return queryset.filter(is_accepted=False)  

        elif self.value() == 'no':
            return queryset.all()


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

from django.utils.html import format_html

@admin.register(Vendor)

class ImageAdmin(admin.ModelAdmin):

    def logo(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.img.url))

    list_display = ['logo' , 'name','creator','start_date','end_date' , 'is_archived']
    readonly_fields = ['creator']
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()
class ViewAdmin(ImportExportModelAdmin):
      
    list_display = ['name','creator','start_date','end_date' , 'is_archived' , 'logo']
    list_filter = [Filter , 'name','start_date']
    search_fields = ['name' , 'creator__username' , 'creator__first_name', 'craetor__last_name']
   
    def auto_archive(self):
        utc=pytz.UTC

        if self.start_date >= utc.localize(datetime.now()):
            self.is_archived = True
            return self.is_archived
    resource_class = VendorResource



@admin.register(Reward)
class View_Admin(ImportExportModelAdmin):
    list_display = ['vendor','points_equivalent' , 'is_archived']
    list_filter = [Filter]
    resource_class = RewardResource

    
@admin.register(budget)
   
class BudgetAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if  not budget.objects.filter(year = datetime.now().year).exists():
            return True
        else:
            return False
   
    fields = ('budget' , 'point' , 'EGP')
    readonly_fields = ('year','budget_compare',)
    list_display = ['budget' , 'year' ,'point', 'EGP' ]

    
    
    def get_queryset(self, request):
        data = super().get_queryset(request)
        to_archive = data.filter(year__lte=datetime.now().year)
        # if to_archive:

            # if datetime.now().year != to_archive[0].year:
            #     to_archive.update(is_archived = True)
            
        return data


@admin.register(budget_in_point)
class budgetPointsAdmin(admin.ModelAdmin):
    list_display = ['current_budget' ,'total_budget', 'year']
    readonly_fields = ('year','total_budget',)
    
    def has_add_permission(self, request):
        return False


@admin.register(Suggest_vendor)
class Viewsuggestion(admin.ModelAdmin):
    list_display = ("vendor","reason","is_archived")
    list_filter = [Filter]

    def has_add_permission(self, request):
            
        return False
@admin.display(description='Status')
def owner(obj):
    return Redemption_Request.objects.filter(status=STATUS[3][0])
@admin.register(Redemption_Request)
class ViewRedemption(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            print(status=STATUS[3][0])
            return redemptionForm(queryset=Redemption_Request.objects.filter(status=STATUS[0][0]))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_display = ("employee" , "voucher" , "request_date" , "status")
    readonly_fields = ["employee", "approved_by" , "request_date" ]
    list_filter = ["status"]
    search_fields = ["employee__username" , "employee__first_name", "employee__last_name" , "voucher__vendor__name"]    
    def save_model(self, request, obj, form, change):
        obj.approved_by = request.user
        obj.save()
    def has_add_permission(self, request):
            
        return False