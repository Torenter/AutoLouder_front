from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import request, HttpResponseRedirect
from .forms import UploadFileForm
# Create your views here.
'''@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section': 'dashboard'})''' #первый вариант страницы личного кабинета
#второй вариант, более рабочий но всё так же непонятный
from django.core.files.storage import FileSystemStorage
@login_required
def dashboard(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')
'''
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@login_required
def dashboard(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render('simple_upload.html', {'form': form})'''