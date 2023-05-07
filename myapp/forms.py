from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file','file_type')
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }
