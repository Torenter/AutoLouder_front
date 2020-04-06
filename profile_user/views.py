from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import request, HttpResponseRedirect, HttpResponseForbidden
from .forms import UploadFileForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

    
class UploadFileCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    template_name = 'simple_upload.html' #путь к шаблону для вывода страницы
    form_class = UploadFileForm
    success_url = reverse_lazy ('dashboard') #куда перенаправлять в случае удачной загрузки файла


@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section': 'dashboard'}) #первый вариант страницы личного кабинета
#второй вариант, более рабочий но всё так же непонятный
'''
from django.core.files.storage import FileSystemStorage
@login_required
def dashboard(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')'''