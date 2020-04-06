from django.db import models
from django.conf import settings

# Create your models here.
class CustomFile(models.Model):
    file_user = models.FileField(upload_to="",)
    status = models.CharField(max_length=50,default='Upload')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank = True,null = True) #- строка приводит к ошибке, но она нужно,чтобы знать какой юзер загрузил файл
    created = models.DateField(auto_now_add=True, db_index=True, blank = True,null = True)