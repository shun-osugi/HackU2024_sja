from django import forms
from .models import Listing
from apps.products.models import UserProfile
from apps.products.models import Product

class ListingForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'subject', 'description', 'price', 'faculty', 'department', 'image']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['account_name', 'email', 'department', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
