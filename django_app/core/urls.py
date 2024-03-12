from django.urls import path
from .views import (
    user_signup_view,
    user_signin_view,
    user_signout_view,
    index_view,
    profile_view,
    user_settings_view,
    create_post_view,
    like_post_view,
    delete_post_view,
)


app_name = 'core'

urlpatterns = [
    path('signup/', user_signup_view, name='user_signup'),
    path('signin/', user_signin_view, name='user_signin'),
    path('signout/', user_signout_view, name='user_signout'),
    path('profile/<str:pk>/', profile_view, name='profile'),
    path('settings/', user_settings_view, name='user_settings'),
    path('create-post/', create_post_view, name='create-post'),
    path('like-post/', like_post_view, name='like-post'),
    path('delete-post/', delete_post_view, name='delete-post'),
    path('', index_view, name='index'),
]
