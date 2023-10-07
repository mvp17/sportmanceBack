from django.db import models
from utils.Singleton import Singleton


# Create your models here.
class EventsKeyWords(Singleton):
    time_ms_name = models.CharField(max_length=50)
    duration_time_ms_name = models.CharField(max_length=50)
    chart_perf_vars = models.TextField(max_length=250)
