from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'پیام خود را اینجا تایپ کنید...',
            'rows': 1,
            'style': 'resize:none;'
        }),
        max_length=1000
    )
