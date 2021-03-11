from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.db.models.fields.files import FileField


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/name file base/<filename>
    if len(instance.file_user_base.name.split('/'))>1:
        my_dir = '{}\\{}'.format(settings.MEDIA_ROOT,instance.file_user_base.name.split('/')[1][:-4])
        if os.path.isdir(my_dir):#проверять существование папки
            if filename in os.listdir(my_dir):# проверяет существование такого же файла в папке как загружаемый
                os.remove(os.path.join(my_dir, filename)) # удаляет файл из папка, если он назыввается так же как загружаемый
        return "{0}/{1}".format(instance.file_user_base.name.split('/')[1][:-4],filename)
    else:
        my_dir = '{}\\{}'.format(settings.MEDIA_ROOT,instance.file_user_base.name[:-4])
        if os.path.isdir(my_dir):#проверять существование папки
            if filename in os.listdir(my_dir):# проверяет существование такого же файла в папке как загружаемый
                os.remove(os.path.join(my_dir, filename)) # удаляет файл из папка, если он назыввается так же как загружаемый
        return "{0}/{1}".format(instance.file_user_base.name[:-4],filename)
# Create your models here.

class CustomFile(models.Model):
    comandas = [
    ('Ruby-RU', 'Ruby-Ru'),
    ('Ruby-EN', 'Ruby-En'),
    ('convert', 'Convert')]
    file_user_param = models.FileField(upload_to=user_directory_path,verbose_name='Param')
    file_user_vars = models.FileField(upload_to=user_directory_path,verbose_name='Vars File')
    file_user_vals = models.FileField(upload_to=user_directory_path,verbose_name='Vals File', null=True, blank=True)
    file_user_weight = models.FileField(upload_to=user_directory_path,verbose_name='Weight File', null=True, blank=True)
    file_user_base = models.FileField(upload_to=user_directory_path,verbose_name='Date Base')
    status = models.CharField(max_length=50,default='Upload')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created = models.CharField(max_length=50,db_index=True)
    name = models.CharField(max_length=50,verbose_name='Название волны/исследования')
    comand = models.CharField(choices=comandas,max_length=50,verbose_name='Параметр формата')
    log = models.CharField(max_length=50,verbose_name='LogFile', default='', null=True, blank=True)