from distutils.log import error
from import_export import resources
from .models import ActivityCategory, User
from django.utils.translation import gettext_lazy as _
import pytz

from django.core.exceptions import ValidationError


class CategoryResource(resources.ModelResource):
    class Meta:
        model = ActivityCategory
        fields = ('category_name','description','start_date','end_date','owner','total_budget')
        import_id_fields = ('category_name',)
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for row in dataset:
        
            pass
            # if row[4] is None or row[3] is None:
            #     error('This field cannot be null.')
                
                  
            # elif row[4] < row[3]:
            #     error('End date should be greater than start date.')
                
                
            # if row[2] is None:
            #     error('This field cannot be null.')

          
            # if row[5] >= row[6] or not row[5] <= row[6]:
            #     print(row[5] >= row[6] or not row[5] <= row[6])

            #     error('Total budget and budget values must be equal.')
                
            
        
    

           
