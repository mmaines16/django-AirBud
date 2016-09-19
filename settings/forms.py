from django import forms
from django.contrib import admin
from models import AirBudConfiguration

class AirBudConfigurationForm(forms.ModelForm):
    conf = AirBudConfiguration.get_solo()

    carrier_dwell_time_seconds = forms.IntegerField(required=True, initial=conf.carrier_dwell_time.seconds)
    carrier_dwell_time_microseconds = forms.IntegerField(required=True, initial=conf.carrier_dwell_time.microseconds)


    class Meta:
        model = AirBudConfiguration
        fields = ('carrier_dwell_time_seconds', 'carrier_dwell_time_microseconds', 'data_check_clicks', 'transmission_check_clicks')
