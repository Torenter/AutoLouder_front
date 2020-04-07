from django import forms
from .models import CustomFile
from django.contrib.auth.models import User
#В принципе форма не нужна, т.к. использутся класс для представления
'''class UploadFileForm(forms.ModelForm):
    class Meta:
        model = CustomFile
        fields = ('file_user',)'''
