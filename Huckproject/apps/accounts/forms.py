from django import forms
from apps.products.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['account_name', 'email', 'department']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@ccmailg.meijo-u.ac.jp'):
            raise forms.ValidationError('許可されていないメールドメインです')
        account_number = email.split('@')[0]
        if not (account_number.isdigit() and len(account_number) == 9):
            raise forms.ValidationError('無効なアカウント番号です')
        return email
