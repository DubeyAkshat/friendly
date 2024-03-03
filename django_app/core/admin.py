from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import UsernameField, UserCreationForm

from .models import User

# Register your models here.


class CustomAdminAuthenticationForm(AdminAuthenticationForm):
    username = forms.CharField(
        label='Email/Username',
        widget=forms.TextInput(attrs={"autofocus": True})
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"
        field_classes = {"username": UsernameField}


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("username", "email", "is_superuser", "is_active")
    list_filter = ("is_superuser", "is_active")
    fieldsets = [
        (None, {"fields": ("email", "username", "date_of_birth", "password",)}),
        ("Personal info", {"fields": ("profile_picture", "bio", "location")}),
        ("Permissions", {"fields": ("is_superuser", "is_active")}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["email", "username", "date_of_birth", "password1", "password2"]}),
        ("Personal info", {"classes": ["wide"], "fields": ["profile_picture", "bio", "location"]}),
        ("Permissions", {"classes": ["wide"], "fields": ["is_superuser"]}),
    ]
    search_fields = ["email", "username", "location"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

class CustomAdminSite(admin.AdminSite):
    login_form = CustomAdminAuthenticationForm

admin_site = CustomAdminSite(name='customadmin')
