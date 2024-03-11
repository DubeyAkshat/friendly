from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.db.models import Q

from .forms import UserSignUpForm, UserSignInForm, UserSettingsForm, CreatePostForm
from .decorators import not_logged_in
from .models import Post

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
    create_post_form = CreatePostForm()
    posts = Post.objects.filter(
        Q(created_by=request.user) | Q(created_by__is_featured=True)
    ).order_by('-created_at')
    return render(
        request,
        'index.html',
        {
            'user': request.user,
            'create_post_form': create_post_form,
            'posts': posts,
        }
    )


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
        return render(request, 'settings.html', {'form': form})


@login_required(login_url='core:user_signin')
@require_http_methods(["POST"])
def create_post_view(request):
    form = CreatePostForm(request.POST, request.FILES)
    print(form)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.user = request.user
        new_post.save()
        return redirect('core:index')
    else:
        return HttpResponse("Invalid request")


@login_required(login_url='core:user_signin')
def like_post_view(request):
    post = get_object_or_404(Post, id=request.GET.get('post_id'))
    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('core:index')


@login_required(login_url='core:user_signin')
def delete_post_view(request):
    post=get_object_or_404(Post, id=request.GET.get('post_id'))
    if post.user == request.user:
        post.delete()
    return redirect('core:index')
