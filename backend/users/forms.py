from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div


class RegistrationForm(UserCreationForm):
     # User fields
    email = forms.EmailField(
        label='Email address', 
        help_text='Your email address'
    )
    
    # Profile fields
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(years=range(1940, 2020)),
        label="Date of Birth"
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Address"
    )
    city = forms.CharField(
        required=False,
        max_length=100,
        label="City"
    )
    country = forms.CharField(
        required=False,
        max_length=100,
        label="Country"
    )
    image = forms.ImageField(
        required=False,
        label="Profile Picture"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('username', css_class='form-control'),
            Field('first_name', css_class='form-control'),
            Field('last_name', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('password1', css_class='form-control'),
            Field('password2', css_class='form-control'),
            Field('date_of_birth', css_class='form-control'),
            Field('address', css_class='form-control'),
            Field('city', css_class='form-control'),
            Field('country', css_class='form-control'),
            Field('image', css_class='form-control'),
        )
        self.helper.add_input(Submit('register', 'Register', css_class='btn btn-primary'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError("Please provide a valid email address")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('login', 'Login', css_class='btn btn-primary'))


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('first_name', css_class='form-control'),
            Field('last_name', css_class='form-control'),
            Field('email', css_class='form-control'),
        )
        self.helper.add_input(Submit('update', 'Update', css_class='btn btn-success'))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'date_of_birth', 'address', 'city', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('image', css_class='form-control'),
            Field('date_of_birth', css_class='form-control'),
            Field('address', css_class='form-control'),
            Field('city', css_class='form-control'),
            Field('country', css_class='form-control'),
        )
        self.helper.add_input(Submit('update_profile', 'Update Profile', css_class='btn btn-success'))


class PasswordChangeFormCustom(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Current Password",
        min_length=8,
        help_text="Enter your current password."
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password",
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password",
        min_length=8,
        help_text="Re-enter the new password for confirmation."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('current_password', css_class='form-control'),
            Field('new_password', css_class='form-control'),
            Field('confirm_new_password', css_class='form-control'),
            Div(
                Submit('change_password', 'Change Password', css_class='btn btn-primary')
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError(
                    "The new passwords do not match."
                )

        return cleaned_data