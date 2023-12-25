from django.db import models

class OcrRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    identification_number = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_issue = models.DateField(blank=True, null=True)
    date_of_expiry = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=(('success', 'Success'), ('failure', 'Failure')))
    error_message = models.TextField(blank=True, null=True)