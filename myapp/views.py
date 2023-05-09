import csv
import json
import pandas as pd
from django.shortcuts import render, redirect,  get_object_or_404
from statsmodels.tsa.arima.model import ARIMA
from .forms import UploadFileForm
from .models import UploadedFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import io
import numpy as np
import matplotlib.pyplot as plt
import zipfile
from django.urls import reverse
from datetime import datetime
import boto3



def store_s3(request, pk):
    aws_access_key_id = 'AKIA4W7FFVFRKSJIONJW'
    aws_secret_access_key = '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'
    region_name = 'us-east-1'
    bucket_name= 'b2photohw2'

    s3 = boto3.client('s3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name)
    media_path = settings.MEDIA_ROOT
    url=media_path + "\\" + pk+"."+"zip"
    print(url)
    with open(url, 'rb') as file:
        s3.put_object(Bucket=bucket_name, Key=pk+"."+"zip", Body=file)


    return render(request, 'store_s3.html')


def sma_csv(cols, window_size):   
    # spark = SparkSession.builder.appName("LoadData").getOrCreate()
    # df = spark.read.csv(db, header=True, inferSchema=True)

    

    # print(db)
    # return cols, window_size
    # time_rows = df.select(cols).collect()
    # time = [row[cols] for row in time_rows]
    print(cols)
    time=cols
    l = len(time)
    sma = np.cumsum(time, dtype=float)
    sma[window_size:] = sma[window_size:] - sma[:-window_size]
    sma = sma[window_size - 1:] / window_size
    sma = sma.tolist()
    for i in range(0,l-len(sma)):
        sma.insert(0,None)
    x=[i for i in range(1,len(sma)+1)]
    y=sma
    return x,y

def arima(series,p,q,d):
    model = ARIMA(series, order=(p, q, d))
    result = model.fit()
    print(result.summary())
    predictions = result.predict(start=0, end=len(series)-1)
    x=[i for i in range(1,len(predictions)+1)]
    return x,predictions


def file_visualize(request, pk):
    print(request.POST)
    file = get_object_or_404(UploadedFile, pk=pk)

    content = file.file.read().decode('utf-8')
    csv_reader = csv.reader(io.StringIO(content))
    
    if request.method ==  'POST':
        print("post", request.POST['conversion_type'])
        if (request.POST['conversion_type']== 'TimeSeries'):
                if (request.POST['model_type']== 'MovingAvg'):
                    column_list = []
                    header = next(csv_reader) 
                    print(header) 
                    ind = header.index(request.POST['mavg_column_name'])
                    for row in csv_reader:
                        column_list.append(float(row[ind]))
                    column_list=column_list[1:]
                    x,y = sma_csv(column_list,int(request.POST['window']))
                    generate_plot(x,column_list,y)  
                
                if (request.POST['model_type']== 'Arima'):
                    p=int(request.POST['p_value'])
                    d=int(request.POST['d_value'])
                    q=int(request.POST['q_value'])
                    col = request.POST['arima_column_name']
                    data_col = request.POST['arima_data_column_name']

                    column_list = []
                    header = next(csv_reader) 
                    print(header) 
                    ind = header.index(col)
                    for row in csv_reader:
                        column_list.append(float(row[ind]))
                    column_list=column_list[1:]
                    x,y = arima(column_list,p,q,d)
                    generate_plot(x,column_list,y) 


                  
        form = UploadFileForm(request.POST, request.FILES)  
            
        return redirect('plot_img')
        # return redirect('file_detail', pk)
        
    else:
        form = UploadFileForm()
    # return render(request, 'upload_file.html', {'form': form})
    return render(request, 'file_visualize.html', {'file': file,'form': form })

def file_list(request):
    files = UploadedFile.objects.all()
    media_path = settings.MEDIA_ROOT
    dirs=[]
    for (dirpath, dirnames, filenames) in os.walk(media_path):
        if os.path.basename(dirpath).endswith(".zip"):
            # Ignore zip folders
            continue
        for dir_name in dirnames:
            if not dir_name.endswith(".zip"):
                dir_path = os.path.join(dirpath, dir_name)
                dir_time = datetime.fromtimestamp(os.path.getmtime(dir_path))
                dir_time = dir_time.strftime('%b %d, %Y %H:%M:%S')
                dirs.append({'name': dir_name, 'url': dir_path, 'size': '-', 'time': dir_time, 'type': 'directory'})
    print(dirs)

    return render(request, 'file_list.html', {'files': files, 'dirs':dirs})

def db_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'db_list.html', {'files': files})

def generate_plot(x,y1,y2):
    if y2==None:
        plt.plot(x,y1)
        file_path = os.path.join(settings.MEDIA_ROOT, 'plot.png')
        plt.savefig(file_path)   
        plt.clf()
    else:
        plt.plot(x,y1)
        plt.plot(x,y2)
        file_path = os.path.join(settings.MEDIA_ROOT, 'plot.png')
        plt.savefig(file_path)   
        plt.clf()
     # fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    # filename = fs.save("plot1.png", img)


def setup_sql_db(request):
    # print(request.POST)
    print(request.POST)
    if request.method == 'POST':
        print("inside post")
         
        return redirect('db_list')



    return render(request, 'setup_sql_db.html')



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
                print("form is valid")
                file_type = form.cleaned_data['local_file_type']
                if(file_type == 'image'):
                    uploaded_file = request.FILES['file']
                    print(uploaded_file)
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                        zip_ref.extractall(settings.MEDIA_ROOT)
                    filename = fs.save(uploaded_file.name, uploaded_file)
                    file_url = fs.url(filename)
                    # uploaded_file_obj = UploadedFile(file=filename, local_file_type=file_type)
                    # uploaded_file_obj.save()
                    

                else:
                    file_type = form.cleaned_data['local_file_type']
                    uploaded_file = request.FILES['file']
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    filename = fs.save(uploaded_file.name, uploaded_file)
                    file_url = fs.url(filename)
                    print(file_url)
                    uploaded_file_obj = UploadedFile(file=filename, local_file_type=file_type)
                    uploaded_file_obj.save()

                    # if (request.POST['conversion_type']== 'TimeSeries'):
                    #     if (request.POST['model_type']== 'MovingAvg'):
                    #         print(sma(file_url,request.POST['mavg_column_name'],int(request.POST['window'])))
                    #         x=[1,2,3,4,5]
                    #         y=[10,20,30,40,50]
                    #         generate_plot(x,y)


                print(request.POST['local_file_type'])
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
    

    
def file_convert(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)
    print(request.POST)
    return render(request, 'file_convert.html', {'file': file})







def plot_img(request):
    return render(request, 'plot_img.html')





def image_list(request, folder):
    folder_path = os.path.join(settings.MEDIA_ROOT, folder)
    images = os.listdir(folder_path)
    images = [image for image in images if not image.endswith('.zip')]
    context = {
        'folder': folder,
        'images': images,
    }
    return render(request, 'image_list.html', context)



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
