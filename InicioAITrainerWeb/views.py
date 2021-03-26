from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group, User
from datetime import *
from .models import Clases_Curso

codes = ['brandsen']


@unauthenticated_user
def index(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            return render(request, "index.html")

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
    context = {
        "form": form
    }
    return render(request, "index.html", context)


def getout(request):
    logout(request)
    return redirect(index)


@allowed_users(allowed_roles=['Premium'])
def trainer(request):
    return render(request, "Trainer.html")


@allowed_users(allowed_roles=['Premium'])
def curso(request):
    obj = Clases_Curso.objects.all()
    context = {
        "clases": obj,
    }

    return render(request, "curso.html", context)


def payment(request, *args, **kwargs):
    if request.method == "POST":
        if request.POST.get('code') in codes:
            group = Group.objects.get(name='Premium')
            request.user.groups.add(group)
            request.user.date_joined = date.today() + timedelta(31)
            request.user.save()

            return redirect(index)
        else:
            return HttpResponseNotFound('<h1>Codigo incorrecto o ya usado.</h1>')
    else:
        return HttpResponseNotFound('<h1>No ingresó un codigo.</h1>')


def month(request, *args, **kwargs):
    if request.method == "POST":
        group = Group.objects.get(name='Premium')
        request.user.groups.add(group)
        if request.POST["text"] == "full month":
            request.user.date_joined = date.today() + timedelta(31)
            request.user.save()
        elif request.POST["text"] == "full week":
            request.user.date_joined = date.today() + timedelta(7)
            request.user.save()
        elif request.POST["text"] == "full year":
            request.user.date_joined = date.today() + timedelta(365)
            request.user.save()
        return redirect(index)
    else:
        return HttpResponseNotFound('<h1>Usted no compró el producto o hubo un problema, contactar al '
                                    'administrador.</h1>')


def FueraTrucho():
    users = User.objects.all()
    for user in users:
        if user.date_joined.date() < date.today():
            group = Group.objects.get(name='Premium')
            user.groups.remove(group)
    return redirect(index)
