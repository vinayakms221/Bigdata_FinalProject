import os
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    local_file_type = models.CharField(max_length=10, choices=(('null','----'),('json', 'JSON'), ('csv', 'CSV'), ('image', 'Image'), ('pdf', 'Document')), blank=True, null=True)
    url_file_type = models.CharField(max_length=10, choices=(('null','----'),('sql', 'SQL'), ('nosql', 'NOSQL')),blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_url = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    conversion_type = models.CharField(max_length=10, choices=(('TimeSeries', 'Time Series'), ('ToSQL', 'To SQL'), ('LinearReg', 'Linear Regression')), blank=True, null=True)
    convert_type = models.CharField(max_length=10, choices=(('ToSQL', 'To SQL'), ('ToNOSQL', 'To NOSQL')), blank=True, null=True)

    collection_name_sql = models.CharField(max_length=255, blank=True, null=True)
    collection_name_nosql = models.CharField(max_length=255, blank=True, null=True)

    X_axis = models.CharField(max_length=255, blank=True, null=True)
    Y_axis = models.CharField(max_length=255, blank=True, null=True)

    mavg_column_name = models.CharField(max_length=255, blank=True, null=True)
    lags_column_name = models.CharField(max_length=255, blank=True, null=True)
    leads_column_name = models.CharField(max_length=255, blank=True, null=True)
    rolling_column_name = models.CharField(max_length=255, blank=True, null=True)
    timereg_column_name = models.CharField(max_length=255, blank=True, null=True)
    arima_column_name = models.CharField(max_length=255, blank=True, null=True)

    lags_data_column_name = models.CharField(max_length=255, blank=True, null=True)
    leads_data_column_name = models.CharField(max_length=255, blank=True, null=True)
    rolling_data_column_name = models.CharField(max_length=255, blank=True, null=True)
    timereg_data_column_name = models.CharField(max_length=255, blank=True, null=True)
    arima_data_column_name = models.CharField(max_length=255, blank=True, null=True)
    window = models.IntegerField(blank=True, null=True)
    lag_amt = models.IntegerField(blank=True, null=True)
    lead_amt = models.IntegerField(blank=True, null=True)
    roll_amt = models.IntegerField(blank=True, null=True)
    lag1_amt = models.IntegerField(blank=True, null=True)
    lag2_amt = models.IntegerField(blank=True, null=True)
    p_value = models.IntegerField(blank=True, null=True)
    q_value = models.IntegerField(blank=True, null=True)
    d_value = models.IntegerField(blank=True, null=True)



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
