from django.apps import AppConfig
from django.conf import settings

class RealtimeSubwayConfig(AppConfig):
    name = 'realtime_subway'

    def ready(self):
        from . import apscheduler
        from .scripts.load_station_data import open_files

        # get station data into the DB.
        # TODO this can probably be done cleaner
        open_files()

        if settings.SCHEDULER_AUTOSTART:
            apscheduler.start()
