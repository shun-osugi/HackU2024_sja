from django import forms
from .models import Listing
from apps.products.models import UserProfile

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['product_name', 'subject', 'description', 'price', 'faculty', 'department', 'image']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['account_name', 'email', 'department', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
