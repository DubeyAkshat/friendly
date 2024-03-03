from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserSignUpForm, UserSignInForm, UserSettingsForm
from .decorators import not_logged_in

# Create your views here.


@not_logged_in
def user_signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:user_settings')
    else:
        form = UserSignUpForm()
    return render(request, 'signup.html', {'form': form})


@not_logged_in
def user_signin_view(request):
    if request.method == 'POST':
        form = UserSignInForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:index')
    else:
        form = UserSignInForm()
    return render(request, 'signin.html', {'form': form})


@login_required(login_url='core:user_signin')
def user_signout_view(request):
    logout(request)
    return redirect('core:user_signin')


@login_required(login_url='core:user_signin')
def index_view(request):
    return render(request, 'index.html')


@login_required(login_url='core:user_signin')
def profile_view(request):
    return render(request, 'profile.html')


@login_required(login_url='core:user_signin')
def user_settings_view(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('core:index')
    else:
        form = UserSettingsForm(instance=request.user)
        return render(request, 'setting.html', {'form': form})
