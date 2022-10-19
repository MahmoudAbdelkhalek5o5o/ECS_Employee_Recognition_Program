from datetime import datetime
from import_export import resources
from .models import Vendors , Rewards
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError
class VendorResource(resources.ModelResource):
    class Meta:
        model = Vendors
        import_id_fields = ('id','name',)
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for row in dataset:
            
            if row[3] < row[2]:
                raise ValidationError(_('End date should be greater than start date.'))

        
class RewardResource(resources.ModelResource):
    class Meta:
        model = Rewards
        import_id_fields = ('id',)
    
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for row in dataset:
            
            if row[2] < row[1]:
                raise ValidationError(_('End date should be greater than start date.'))