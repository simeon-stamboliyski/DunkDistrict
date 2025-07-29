from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control-custom', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control-custom', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control-custom', 'placeholder': 'Enter your email address'}),
            'subject': forms.Select(attrs={'class': 'form-control-custom'}),
            'message': forms.Textarea(attrs={'class': 'form-control-custom', 'rows': 6, 'placeholder': 'Enter your message here...'}),
        }