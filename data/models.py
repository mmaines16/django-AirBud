from __future__ import unicode_literals

from django.db import models

# Create your models here.
class WindData(models.Model):
    wind_direction = models.IntegerField(null=False, blank=True, default=0)
    wind_speed = models.DecimalField(null=False, blank=True, default=0.0, max_digits=3, decimal_places=2)
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
