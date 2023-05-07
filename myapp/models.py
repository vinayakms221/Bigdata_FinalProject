import os
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=(('json', 'JSON'), ('csv', 'CSV'), ('image', 'Image')))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.file_type = self.get_file_type(self.file.name)
        super(UploadedFile, self).save(*args, **kwargs)

    def get_file_type(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.csv':
            return 'csv'
        elif ext == '.json':
            return 'json'
        elif ext in ('.jpg', '.jpeg', '.png', '.gif'):
            return 'image'
        else:
            return 'unknown'
