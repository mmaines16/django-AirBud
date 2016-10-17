from __future__ import unicode_literals

from django.db import models

# Create your models here.
class WindData(models.Model):
    wind_direction = models.IntegerField(null=False, blank=True, default=0)
    variable_wind_direction_max = models.IntegerField(null=False, blank=True, default=0)
    variable_wind_direction_min = models.IntegerField(null=False, blank=True, default=0)
    wind_speed = models.DecimalField(null=False, blank=True, default=0.0, max_digits=3, decimal_places=2)
    wind_gust = models.DecimalField(null=False, blank=True, default=0.0, max_digits=3, decimal_places=2)
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __unicode__(self):
        date = str(self.time_stamp.date())
        hour = str(self.time_stamp.time().hour)
        minute = str(self.time_stamp.time().minute)
        second = str(self.time_stamp.time().second)
        microsecond = str(self.time_stamp.time().microsecond)
        return "Date: " + date + " Time: " + hour + "-" + minute + "-" + second + " (" + microsecond + ")"
