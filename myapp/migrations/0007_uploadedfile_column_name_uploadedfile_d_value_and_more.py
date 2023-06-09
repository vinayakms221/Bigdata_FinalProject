# Generated by Django 4.2 on 2023-05-08 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_uploadedfile_x_axis_uploadedfile_y_axis_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='column_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='d_value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='data_column_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='lag1_amt',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='lag2_amt',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='lag_amt',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='lead_amt',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='p_value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='q_value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='roll_amt',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='window',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
