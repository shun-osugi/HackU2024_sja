# forms.py (transactionsアプリ)
from django import forms
from .models import Transaction, Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class MeetingTimeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['meeting_time']