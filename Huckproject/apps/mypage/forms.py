from django import forms
from apps.transactions.models import Message, Transaction

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class MeetingTimeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['meeting_time']
        widgets = {
            'meeting_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }