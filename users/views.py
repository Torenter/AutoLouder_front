from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def persone(required):
    return render (request,)# дописать куда перенаправлять пользователя после успешной авторизации