from __future__ import absolute_import      #from Python 3 import the absolute_import module so celery.py will not clash with
                                            # with the library

import os                                   # allow for operating system file manipulation

from celery import Celery                   # import the Celery object from the celery python library

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'air_bud.settings')

from django.conf import settings            # Import the django settings from setting.py

app = Celery('air_bud')                     # create a Celery application for all of the async tasks to run under "air_bud"

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')              # Tell Celery to use the configuration settings from settings.py
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)     # Tell Celery to include all installed application modules to this app
#Django Celery settings
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)

@app.task(bind=True)                        # Use the app.task decorator to make the following function a Celery Task
def debug_task(self):                       # Function to test if Celery is running correctly
    print('Request: {0!r}'.format(self.request))
