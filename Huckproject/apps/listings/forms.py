from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['product_name', 'subject', 'description', 'price', 'faculty', 'department', 'image']
