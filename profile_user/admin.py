from django.contrib import admin
from .models import CustomFile
# Register your models here.
@admin.register(CustomFile)
class CustomFileAdmin(admin.ModelAdmin):
    list_display=['file_user','status','created','user']
    list_filter = ['status','user']