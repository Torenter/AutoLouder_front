from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import request, HttpResponseRedirect, HttpResponseForbidden
#from .forms import UploadFileForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomFile
from django.conf import settings
#from django.contrib.auth.models import User
#from django.urls import reverse
import socket
from datetime import datetime
    
class UploadFileCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = CustomFile
    fields = ['file_user_base','file_user_vars','file_user_vals','file_user_weight','file_user_param'] #Поле выводимое на экран из модели
    template_name = 'simple_upload.html' #путь к шаблону для вывода страницы
    success_url = reverse_lazy ('dashboard') #куда перенаправлять в случае удачной загрузки файла
    def form_valid(self, form ):
        form.instance.user = self.request.user # автозаполнение поля пользователя
        form.instance.created = str(datetime.now()) # автозаполнение поля даты
        file_name = self.request.FILES['file_user_base'].name # в request.FILES хранится всё о файле. Через ключ мы обращаемся к полю с файлом, где содержится вся информация. И берет атрибут имени,чтобы знать как файл называется
        body=f'{settings.MEDIA_ROOT}\\{file_name[:-4]};{form.instance.created}' 
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect(('127.0.0.1',9090))
        sock.send(body.encode('utf-8'))
        sock.close()
        return super().form_valid(form)    

@login_required
def dashboard(request):
    post = CustomFile.objects.filter(user=request.user)
    return render(request,'account/dashboard.html',{'post': post}) #первый вариант страницы личного кабинета
