from __future__ import unicode_literals

from django.db import models
from solo.models import SingletonModel

from datetime import timedelta #Python module used to set the default values for models.DurationField

#set the default carrier dwell time to be 2.5 seconds
DEFAULT_CARRIER_DWELL_TIME_MIN = timedelta(seconds=0, microseconds=10000)
DEFAULT_CARRIER_DWELL_TIME_MAX = timedelta(seconds=2, microseconds=0)
DEFAULT_CARRIER_INTERVAL_TIME_MIN = timedelta(seconds=0, microseconds=100000)
DEFAULT_CARRIER_INTERVAL_TIME_MAX = timedelta(seconds=2, microseconds=0)

# Create your models here.
class AirBudConfiguration(SingletonModel):
    carrier_dwell_time_min = models.DurationField(blank=False, null=False, default=DEFAULT_CARRIER_DWELL_TIME_MIN)
    carrier_dwell_time_max = models.DurationField(blank=False, null=False, default=DEFAULT_CARRIER_DWELL_TIME_MAX)
    carrier_interval_time_min = models.DurationField(blank=False, null=False, default=DEFAULT_CARRIER_INTERVAL_TIME_MIN)
    carrier_interval_time_max = models.DurationField(blank=False, null=False, default=DEFAULT_CARRIER_INTERVAL_TIME_MAX)
    weather_check_clicks = models.IntegerField(blank=False, null=False, default=4)
    transmission_check_clicks = models.IntegerField(blank=False, null=False, default=3)
    report_gust = models.IntegerField(blank=False, null=False, default=3)
    report_variable_winds = models.IntegerField(blank=False, null=False, default=15) #in Degrees
    update_direction = models.IntegerField(blank=False, null=False, default=30)
    update_speed = models.IntegerField(blank=False, null=False, default=5)
    update_timer = models.IntegerField(blank=False, null=False, default=5)
    cross_wind_limit_speed = models.IntegerField(blank=False, null=False, default=6)
    cross_wind_limit_direction = models.IntegerField(blank=False, null=False, default=45)
    favor_wind_speed = models.IntegerField(blank=False, null=False, default=6)
    favor_wind_direction = models.IntegerField(blank=False, null=False, default=44)
