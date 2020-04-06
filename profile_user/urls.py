from django.urls import path
from .views import UploadFileCreateView, dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'), 
    path('simple_upload/',UploadFileCreateView.as_view(),name = 'add'),

]