from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file','local_file_type', 'url_file_type')
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }
# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = UploadedFile
#         fields = ('file','file_type', 'file_url')
