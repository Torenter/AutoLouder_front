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
import pika
    
class UploadFileCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = CustomFile
    fields = ['file_user'] #Поле выводимое на экран из модели
    template_name = 'simple_upload.html' #путь к шаблону для вывода страницы
    success_url = reverse_lazy ('dashboard') #куда перенаправлять в случае удачной загрузки файла
    def form_valid(self, form ):
        form.instance.user = self.request.user # автозаполнение поля пользователя
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue= 'hello')
        file_name=self.request.FILES['file_user'].name # в request.FILES хранится всё о файле. Через ключ мы обращаемся к полю с файлом, где содержится вся информация. И берет атрибут имени,чтобы знать как файл называется
        channel.basic_publish(exchange='', routing_key='hello', body='{}\\{}'.format(settings.MEDIA_ROOT,file_name )) #отправка сообщения с дирректорией и названием файла

        channel.close()
        return super().form_valid(form)
    

@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section': 'dashboard'}) #первый вариант страницы личного кабинета
