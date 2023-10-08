from django.db import models


# Create your models here.
class DataInput(models.Model):
    title = models.CharField(max_length=100, blank=True)
    athlete = models.CharField(max_length=100, blank=True)
    csv = models.FileField(upload_to='csv_files/')
    is_event_file = models.BooleanField()
    frequency = models.PositiveIntegerField()
