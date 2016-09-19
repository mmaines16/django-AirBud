from __future__ import unicode_literals

from django.db import models
from solo.models import SingletonModel

from datetime import timedelta #Python module used to set the default values for models.DurationField

#set the default carrier dwell time to be 2.5 seconds
DEFAULT_CARRIER_DWELL_TIME = timedelta(seconds=2, microseconds=50000)

# Create your models here.
class AirBudConfiguration(SingletonModel):
    carrier_dwell_time = models.DurationField(blank=False, null=False, default=DEFAULT_CARRIER_DWELL_TIME)
    data_check_clicks = models.IntegerField(blank=False, null=False, default=4)
    transmission_check_clicks = models.IntegerField(blank=False, null=False, default=3)
