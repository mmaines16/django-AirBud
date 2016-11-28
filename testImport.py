import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "air_bud.settings")
django.setup()

from settings.models import AirBudConfiguration

conf = AirBudConfiguration.get_solo()

print conf.carrier_dwell_time

print "Hello World!"
