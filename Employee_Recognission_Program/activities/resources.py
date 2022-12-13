from distutils.log import error
from import_export import resources
from .models import ActivityCategory, User , Activity
from django.utils.translation import gettext_lazy as _
import pytz
from Rewards.models import budget , budget_in_point
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import Sum

from django.contrib import messages

class CategoryResource(resources.ModelResource):
    class Meta:
        model = ActivityCategory
        fields = ('category_name','description','start_date','end_date','owner','threshhold')
        import_id_fields = ('category_name',)
        
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        
        total = 0
        
        
            
class ActivityResource(resources.ModelResource):
    class Meta:
        model = Activity
        fields = ('activity_name','activity_description','category','points','evidence_needed','start_date','end_date','owner','total_budget')
        import_id_fields = ('activity_name',)
            
        
    

           
