# Generated by Django 4.2 on 2023-05-07 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_uploadedfile_file_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
