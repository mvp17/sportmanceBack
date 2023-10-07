from django.db import models
from utils.Singleton import Singleton


# Create your models here.
class DevicesKeyWords(Singleton):
    time_name = models.CharField(max_length=40)
