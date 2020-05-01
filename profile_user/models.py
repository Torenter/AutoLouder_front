from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/name file base/<filename>
    return '{0}/{1}'.format(instance.file_user_base.name,filename)
# Create your models here.
class CustomFile(models.Model):
    '''через verbose задать строки,которык будут отображены на сайте'''
    file_user_param = models.FileField(upload_to=user_directory_path)
    file_user_vars = models.FileField(upload_to=user_directory_path)
    file_user_vals = models.FileField(upload_to=user_directory_path)
    file_user_weight = models.FileField(upload_to=user_directory_path)
    file_user_base = models.FileField(upload_to=user_directory_path,verbose_name='File for base')
    status = models.CharField(max_length=50,default='Upload')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, db_index=True)
   