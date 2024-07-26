from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseNotFound


def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseNotFound(render(request, '404.html'))
    return wrapper

def supervisor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_supervisor:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseNotFound(render(request, '404.html'))
    return wrapper

def no_supervisor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_supervisor:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseNotFound(render(request, '404.html'))
    return wrapper