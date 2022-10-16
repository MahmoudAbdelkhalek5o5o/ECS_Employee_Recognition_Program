from import_export import resources
from .models import User

class UsersResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('id')
        import_id_fields = ('emp_id','email',)
    
    