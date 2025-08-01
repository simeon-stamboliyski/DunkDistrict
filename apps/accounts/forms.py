from django import forms
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control-custom'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control-custom'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control-custom'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control-custom'}),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control-custom'}),
        label='Confirm Password'
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control-custom'}),
        label='Date of Birth'
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')
    password = forms.CharField(widget=forms.PasswordInput)