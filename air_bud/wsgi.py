"""
WSGI config for air_bud project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys
import djcelery

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www')
sys.path.append('/var/www/airbud')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "air_bud.settings")

djcelery.setup_loader()

application = get_wsgi_application()
