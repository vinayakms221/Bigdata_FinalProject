"""
URL configuration for Final_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp.views import file_list, upload_file, file_detail, file_convert, file_visualize, plot_img, db_list, setup_sql_db, store_s3
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', file_list, name='file_list'),
    path('dblist/', db_list, name='db_list'),
    path('upload/', upload_file, name='upload_file'),
    path('uploads/<int:pk>/', file_detail, name='file_detail'),
    path('convert/<int:pk>/', file_convert, name='file_convert'),
    path('visualize/<int:pk>/', file_visualize, name='file_visualize'),
    path('plot/', plot_img, name='plot_img'),
    path('sqlform/', setup_sql_db, name='setup_sql_db'),
    path('success/<str:pk>/', store_s3, name='store_s3'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
