from django.contrib import admin

from models import WindData

# Register your models here.
class WindDataAdmin(admin.ModelAdmin):
    readonly_fields = (
    'wind_direction',
    'variable_wind_direction_max',
    'variable_wind_direction_min',
    'wind_speed',
    'wind_gust',
    'time_stamp'
    )
    class Meta:
        model = WindData
        exclude = ()

admin.site.register(WindData, WindDataAdmin)
