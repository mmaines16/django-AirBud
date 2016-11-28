from django import forms
from django.contrib import admin
from models import AirBudConfiguration

class AirBudConfigurationForm(forms.ModelForm):
    conf = AirBudConfiguration.get_solo()

    carrier_dwell_time_min_seconds = forms.IntegerField(required=True, initial=conf.carrier_dwell_time_min.seconds)
    carrier_dwell_time_min_microseconds = forms.IntegerField(required=True, initial=conf.carrier_dwell_time_min.microseconds)


    class Meta:
        model = AirBudConfiguration
        fields = ('carrier_dwell_time_min_seconds', 'carrier_dwell_time_min_microseconds', 'weather_check_clicks', 'transmission_check_clicks')
