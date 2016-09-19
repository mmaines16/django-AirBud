from __future__ import absolute_import      #from Python 3 import the absolute_import module so celery.py will not clash with
                                            # with the library

from .celery import app as celery_app       # Make sure the app is always imported when Django starts up so all tasks will be
                                            # under the "shared_task" to allow for reusable modules. This way we dont have to
                                            # load our unique application instance whenever we want to create a Task, we can
                                            # instead use the @shared_task decorator to make a function a task 
