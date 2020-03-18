from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import request
# Create your views here.
@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section': 'dashboard'})