from functools import wraps
from django.shortcuts import render, redirect


def not_logged_in(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('core:index')
    return wrapper
