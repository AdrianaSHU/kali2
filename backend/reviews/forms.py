from django import forms
from .models import Review

# Form for Contact Us Page
class InquiryForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Your Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}),
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
    )
    subject = forms.CharField(
        max_length=200,
        label="Subject",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the subject of your inquiry'}),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your message here...'}),
    )

# Form for Submitting Reviews
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }
