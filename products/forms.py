from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'stars']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'نظر خود را بنویسید...'
            }),
            'stars': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'body': 'متن نظر',
            'stars': 'امتیاز شما'
        }












