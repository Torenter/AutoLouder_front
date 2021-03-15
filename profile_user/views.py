from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import request, HttpResponseRedirect, HttpResponseForbidden, HttpResponse
#from .forms import UploadFileForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomFile
from django.conf import settings
#from django.contrib.auth.models import User
#from django.urls import reverse
import socket
from datetime import datetime
import json, os
    
class UploadFileCreateView(LoginRequiredMixin,CreateView):
    """Осуществляет загрузку файлов на сервер"""
    login_url = '/login/'
    model = CustomFile
    fields = ['file_user_base','file_user_vars','file_user_vals','file_user_weight','file_user_param','name','comand'] #Поле выводимое на экран из модели
    template_name = 'simple_upload.html' #путь к шаблону для вывода страницы
    success_url = '/autoloader/'
    #куда перенаправлять в случае удачной загрузки файла
    def form_valid(self, form):
        form.instance.user = self.request.user # автозаполнение поля пользователя
        form.instance.created = str(datetime.now()) # автозаполнение поля даты
        file_name = self.request.FILES['file_user_base'].name # в request.FILES хранится всё о файле. Через ключ мы обращаемся к полю с файлом, где содержится вся информация. И берет атрибут имени,чтобы знать как файл называется
        if form.instance.comand[:4] == 'Ruby': # если команда Руби, нужно вытащить параметр ланга
            comand,lang = form.instance.comand.split('-') 
            body = {'path':settings.MEDIA_ROOT,'name':file_name[:-4],'key':form.instance.created,'comand':comand,'lang':lang} #Собирает словарь
        else:
            body = {'path':settings.MEDIA_ROOT,'name':file_name[:-4],'key':form.instance.created,'comand':form.instance.comand,'lang':""} #Собирает словрь
        body = json.dumps(body) #Превращает словарь в json строку
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.connect(('127.0.0.1',50000))
            sock.send(body.encode('utf-8')) #кодируем в utf-8 для меньших заморочек с байтами
            sock.close()
            return super().form_valid(form)
        except ConnectionRefusedError:
            return HttpResponse(status=522)

@login_required
def dashboard(request):
    """Главная страница, с отображением всех записей пользователя"""
    post = CustomFile.objects.filter(user=request.user)
    return render(request,'account/dashboard.html',{'post': post}) #первый вариант страницы личного кабинета

class ChangeFile(LoginRequiredMixin,UpdateView):
    """Форма обновления записи(перезагрузки файлов)"""
    model = CustomFile
    fields = fields = ['file_user_base','file_user_vars','file_user_vals','file_user_weight','comand']
    template_name = 'files_update_form.html'
    success_url = '/autoloader/'
    def form_valid(self, form):
        file_name = form.instance.file_user_base.name.split('/')[0] # в request.FILES хранится всё о файле. Через ключ мы обращаемся к полю с файлом, где содержится вся информация. И берет атрибут имени,чтобы знать как файл называется
        form.instance.status = "Reload"
        if form.instance.comand[:4] == 'Ruby': # если команда Руби, нужно вытащить параметр ланга
            comand,lang = form.instance.comand.split('-') 
            body = {'path':settings.MEDIA_ROOT,'name':file_name,'key':form.instance.created,'comand':comand,'lang':lang} #Собирает словарь
        else:
            body = {'path':settings.MEDIA_ROOT,'name':file_name,'key':form.instance.created,'comand':form.instance.comand,'lang':""} #Собирает словрь
        body = json.dumps(body) #Превращает словарь в json строку
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.connect(('127.0.0.1',50000))
            sock.send(body.encode('utf-8')) #кодируем в utf-8 для меньших заморочек с байтами
            sock.close()
            return super().form_valid(form)
        except ConnectionRefusedError:
            return HttpResponse(status=522)

@login_required
def showLog(request):
    s = request.GET['name'].split('/')[0]
    if os.path.isdir(f'{settings.MEDIA_ROOT}\\{s}'):#проверять существование папки:
        if 'log.txt' in os.listdir(f'{settings.MEDIA_ROOT}\\{s}'):#проверять существование файла:
            f = open(f'{settings.MEDIA_ROOT}\\{s}\\log.txt', 'r',encoding='windows-1251')
            file_content = f.read()
            file_content = file_content.split('\n')
            f.close()
            context = {'file_content': file_content}
            return render(request, "log.html", context)
        else:
            return HttpResponse('<h1>Page was not found</h1>')
    else:
        return HttpResponse('<h1>Page was not found</h1>')