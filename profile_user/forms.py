from django import forms
from .models import CustomFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = CustomFile
        fields = ('file_user',)
