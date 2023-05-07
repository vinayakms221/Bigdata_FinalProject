from django.test import TestCase
from django.urls import reverse
from .models import UploadedFile

class UploadedFileModelTests(TestCase):
    def test_file_type(self):
        file = UploadedFile.objects.create(file='test.csv')
        self.assertEqual(file.local_file_type, 'csv')

class FileUploadTests(TestCase):
    def test_upload_csv(self):
        with open('test.csv', 'rb') as f:
            response = self.client.post(reverse('upload_file'), {'file': f})
        self.assertRedirects(response, reverse('file_list'))
        self.assertEqual(UploadedFile.objects.count(), 1)
        file = UploadedFile.objects.first()
        self.assertEqual(file.local_file_type, 'csv')

    def test_upload_image(self):
        with open('test.png', 'rb') as f:
            response = self.client.post(reverse('upload_file'), {'file': f})
        self.assertRedirects(response, reverse('file_list'))
        self.assertEqual(UploadedFile.objects.count(), 1)
        file = UploadedFile.objects.first()
        self.assertEqual(file.local_file_type, 'image')
