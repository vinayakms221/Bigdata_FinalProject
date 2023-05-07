
# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import UploadedFile

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'file_size', 'uploaded_at')
    list_filter = ('file_type',)
    search_fields = ('file',)
    readonly_fields = ('uploaded_at',)

    def file_name(self, obj):
        return format_html('<a href="{}">{}</a>', obj.file.url, obj.file.name)

    def file_size(self, obj):
        return format_html('{:.2f} KB', obj.file.size / 1024)
    file_size.short_description = 'Size'
