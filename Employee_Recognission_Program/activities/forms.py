from django import forms
from django.forms import ModelForm
from .models import ActivityCategory , Activity
from Users.models import User
class CategoryForm(forms.ModelChoiceField):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            return CategoryForm(queryset=User.objects.filter(is_active = True))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

            

