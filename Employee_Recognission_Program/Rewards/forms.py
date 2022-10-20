from .models import Vendors , Rewards
from django import forms
from .models import Role
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

class UserForm(forms.ModelForm):
    class Meta:
        model = Vendors

    def clean(self):
        username = self.cleaned_data.get('username')
        vendor_policy = self.cleaned_data.get('vendor_policy')
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        creator  = self.cleaned_data.get('creator')
        accepts_voucher = self.cleaned_data.get('accepts_voucher')
        img = self.cleaned_data.get('img')
        accepts_procurement = self.cleaned_data.get('accepts_procurement')
        accepts_direct = self.cleaned_data.get('accepts_direct')
        
        if end_date < start_date:
            
            raise forms.ValidationError(_('End date should be greater than start date.'))
        return self.cleaned_data
    
class UserForm(forms.ModelForm):
    class Meta:
        model = Vendors

    def clean(self):
        username = self.cleaned_data.get('username')
        vendor_policy = self.cleaned_data.get('vendor_policy')
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        creator  = self.cleaned_data.get('creator')
        accepts_voucher = self.cleaned_data.get('accepts_voucher')
        img = self.cleaned_data.get('img')
        accepts_procurement = self.cleaned_data.get('accepts_procurement')
        accepts_direct = self.cleaned_data.get('accepts_direct')
        
        if end_date < start_date:
            
            raise forms.ValidationError(_('End date should be greater than start date.'))
        return self.cleaned_data