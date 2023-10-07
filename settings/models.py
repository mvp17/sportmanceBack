from django.db import models
from utils.Singleton import Singleton


# Create your models here.
class SessionParameters(Singleton):
    init_time_ms = models.PositiveIntegerField()
    fin_time_ms = models.PositiveIntegerField()
    frequency = models.PositiveIntegerField()
