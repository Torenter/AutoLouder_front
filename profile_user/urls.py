from django.urls import path
from .views import UploadFileCreateView, dashboard, ChangeFile, showLog

urlpatterns = [
    path('simple_upload/',UploadFileCreateView.as_view(),name = 'add'),
    path('<int:pk>/',ChangeFile.as_view(),name = 'update_form'),
    path('log/',showLog,name = 'showLog'),
    path('', dashboard, name='dashboard'),
]