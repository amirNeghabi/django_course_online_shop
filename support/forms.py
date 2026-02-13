# support/forms.py
from django import forms
from .models import Ticket, TicketMessage, TicketCategory

class TicketCreateForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows':4, 'placeholder':'متن درخواست خود را بنویسید...'}),
        label='پیام'
    )
    
    class Meta:
        model = Ticket
        fields = ['category', 'subject']
        widgets = {
            'category': forms.Select(attrs={'class':'form-select'}),
            'subject': forms.TextInput(attrs={'class':'form-control', 'placeholder':'موضوع تیکت'}),
        }

class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows':3, 'class':'form-control', 'placeholder':'پاسخ خود را بنویسید...'}),
        }
