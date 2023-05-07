import os
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    local_file_type = models.CharField(max_length=10, choices=(('json', 'JSON'), ('csv', 'CSV'), ('image', 'Image'), ('pdf', 'Document')), blank=True, null=True)
    url_file_type = models.CharField(max_length=10, choices=(('sql', 'SQL'), ('nosql', 'NOSQL')),blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_url = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    # def __str__(self):
    #     retString = ""
    #     if self.file:
    #         retString += str(self.file)
    #     else:
    #         retString += "None"
    #     print(f"{retString}")


    def save(self, *args, **kwargs):
        self.local_file_type = self.get_file_type(self.file.name)
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
