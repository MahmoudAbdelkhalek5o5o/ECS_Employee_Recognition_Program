from import_export import resources
from .models import Vendors

class VendorResource(resources.ModelResource):
    class Meta:
        model = Vendors
        import_id_fields = ('id')