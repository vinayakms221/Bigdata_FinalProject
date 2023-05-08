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
import numpy as np
import matplotlib.pyplot as plt

def sma(db, cols, window_size):   
    # spark = SparkSession.builder.appName("LoadData").getOrCreate()
    # df = spark.read.csv(db, header=True, inferSchema=True)
    print(db)
    return db, cols, window_size
    # time_rows = df.select(cols).collect()
    # time = [row[cols] for row in time_rows]
        
    # l = len(time)
    # sma = np.cumsum(time, dtype=float)
    # sma[window_size:] = sma[window_size:] - sma[:-window_size]
    # sma = sma[window_size - 1:] / window_size
    # sma = sma.tolist()
    # for i in range(0,l-len(sma)):
    #     sma.insert(0,None)
    # return sma

def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})

def generate_plot(x,y):
    plt.plot(x,y)
    file_path = os.path.join(settings.MEDIA_ROOT, 'plot1.png')
    plt.savefig(file_path)    # fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    # filename = fs.save("plot1.png", img)



def upload_file(request):
    # form = None
    print(request.POST)
    # print("abc")
    if request.method == 'POST':
        print("post", request.POST['upload_option'])
        if 'local' == request.POST['upload_option']:
            
            form = UploadFileForm(request.POST, request.FILES)
            # print("local", form, form.is_valid())
            if form.is_valid():
                file_type = form.cleaned_data['local_file_type']
                uploaded_file = request.FILES['file']
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_url = fs.url(filename)
                uploaded_file_obj = UploadedFile(file=filename, local_file_type=file_type)
                uploaded_file_obj.save()

                if (request.POST['conversion_type']== 'TimeSeries'):
                    if (request.POST['model_type']== 'MovingAvg'):
                        print(sma(file_url,request.POST['mavg_column_name'],int(request.POST['window'])))
                        x=[1,2,3,4,5]
                        y=[10,20,30,40,50]
                        generate_plot(x,y)


                # print(request.POST['conversion_type'])
                return redirect('file_list')
        elif 'url' == request.POST['upload_option']:
            print("url")
            url = request.POST['file_url']
            file_type = request.POST['url_file_type']
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            # uploaded_file_obj = UploadedFile(file=url, url_file_type=file_type)
            # uploaded_file_obj.save()
            return redirect('file_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file_type = form.cleaned_data['file_type']
#             print(file_type)
#             uploaded_file = request.FILES['file']
#             fs = FileSystemStorage(location=settings.MEDIA_ROOT)
#             filename = fs.save(uploaded_file.name, uploaded_file)
#             file_url = fs.url(filename)
#             uploaded_file_obj = UploadedFile(file=filename, file_type=file_type)
#             uploaded_file_obj.save()
#             return redirect('file_list')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload_file.html', {'form': form})


def file_detail(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)
    if file.local_file_type == 'csv':
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
        print(file.local_file_type)
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
