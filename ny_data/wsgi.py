"""
WSGI config for ny_data project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from realtime_subway.apscheduler import start
from realtime_subway.scripts.load_station_data import import_station_data

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ny_data.settings')

application = get_wsgi_application()

# Populate DB with station data on startup
import_station_data()
# Begin the train data import scheduler
# start()
