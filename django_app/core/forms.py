from django import forms 
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.admin.forms import AdminAuthenticationForm
from django.utils.translation import gettext_lazy as _

from .models import User, Post


class UserSignUpForm(UserCreationForm): 
    class Meta:
        model = User
        fields = ('email', 'username', 'date_of_birth')
        widgets = {
            'email': forms.EmailInput(attrs={'autofocus': True}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'label': 'Date of Birth'}),
        }

    field_order = [
        'email',
        'username',
        'date_of_birth',
        'password1',
        'password2'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label


class UserSignInForm(AuthenticationForm):
    username = forms.CharField(label='Email/Username', widget=forms.TextInput(attrs={"autofocus": True}))

    error_messages = {
        "invalid_login": _(
            "Invalid credentials"
        ),
        "inactive": _("This account is inactive."),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username', 
            'date_of_birth', 
            'profile_picture', 
            'bio', 
            'location',
        )
        widgets = {
            'email': forms.EmailInput(attrs={'autofocus': True}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        field_classes = {"username": UsernameField}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        current_username = self.instance.username

        # Check if the entered username is different from the current one
        if username.lower() != current_username.lower():
            if User.objects.filter(username__iexact=username).exists():
                self.add_error("username", self.instance.unique_error_message(User, ["username"]))
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        current_email = self.instance.email

        # Check if the entered email is different from the current one
        if email.lower() != current_email.lower():
            if User.objects.filter(email__iexact=email).exists():
                self.add_error("email", self.instance.unique_error_message(User, ["email"]))
        return email


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'image',
            'caption',
        )
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 5}),
        }
