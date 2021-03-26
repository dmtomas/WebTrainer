from django.http import HttpResponse
from django.shortcuts import redirect, render
from datetime import *

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            context = {
                "premium": group
            }
            return render(request, "LogIndex.html", context)
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("No estas autorizado a ver la pagina")
        return wrapper_func
    return decorator
