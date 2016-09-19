from django.contrib import admin
from models import AirBudConfiguration
from solo.admin import SingletonModelAdmin
from forms import AirBudConfigurationForm

# Register your models here.
class AirBudConfigurationAdmin(SingletonModelAdmin):
    exclude = ('carrier_dwell_time',)
    class Meta:
        model = AirBudConfiguration
        form = AirBudConfigurationForm

    #def save_model(self, request, obj, form, change):
        #obj.

admin.site.register(AirBudConfiguration, AirBudConfigurationAdmin)
