from distutils.log import error
from import_export import resources
from .models import ActivityCategory, User , Activity
from django.utils.translation import gettext_lazy as _
import pytz
from Rewards.models import budget
from django.core.exceptions import ValidationError
from datetime import datetime


class CategoryResource(resources.ModelResource):
    class Meta:
        model = ActivityCategory
        fields = ('category_name','description','start_date','end_date','owner','total_budget')
        import_id_fields = ('category_name',)
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        
        total = 0
        Budget = budget.objects.filter(year = datetime.now().year)[0].budget

        for row in dataset.dict:
            total += row["total_budget"]
            if total > Budget:
                raise ValidationError(_("Budget exceeded the limit"))
            
class ActivityResource(resources.ModelResource):
    class Meta:
        model = Activity
        fields = ('activity_name','activity_description','category','points','evidence_needed','start_date','end_date','owner','total_budget')
        import_id_fields = ('activity_name',)
            
        
    

           
