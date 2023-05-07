import csv
import json
import pandas as pd
from django.shortcuts import render, redirect,  get_object_or_404
from .forms import UploadFileForm
from .models import UploadedFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import io



def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_type = form.cleaned_data['file_type']
            print(file_type)
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)
            uploaded_file_obj = UploadedFile(file=filename, file_type=file_type)
            uploaded_file_obj.save()
            return redirect('file_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})


def file_detail(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)
    if file.file_type == 'csv':
        # content = file.file.read().decode('ISO-8859-1')
        # # use pandas to read the CSV data and create a DataFrame
        # df = pd.read_csv(io.StringIO(content))
        # # convert the DataFrame to an HTML table
        # table = df.to_html(index=False)
        # return render(request, 'file_detail.html', {'file': file, 'table': table})
        content = file.file.read().decode('utf-8')
        reader = csv.reader(io.StringIO(content), delimiter=';')
        rows = [row for row in reader]
        # print(rows)
        print(file.file_type)
        return render(request, 'file_detail.html', {'file': file, 'rows': rows})
    # elif file.file_type in ['jpg', 'jpeg', 'png', 'gif']:
    else:
        print(file.file)
        return render(request, 'file_detail.html', {'file': file})




    # Handle other file types here

    return redirect('file_list')

def handle_uploaded_file(file, file_type):
    filename = file.name
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    uploaded_file = UploadedFile(file=file_path, file_type=file_type)
    uploaded_file.save()


def handle_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def handle_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        print(data)

def handle_image_files(file_path):
    # Handle multiple image files in the uploaded folder
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                print(os.path.join(root, file))