from django.apps import AppConfig
from django.conf import settings

class RealtimeSubwayConfig(AppConfig):
    name = 'realtime_subway'

    def ready(self):
        # This is a common hook to init certain app pieces on django startup
        # however this is run whenever manage.py is invoked? which causes 
        # certain operations (ie migrating DB) to fail due to entrypoint.sh
        
        # from . import apscheduler
        # from .scripts.load_station_data import import_station_data

        # get station data into the DB.
        # TODO this can probably be done cleaner
        # import_station_data()

        # if settings.SCHEDULER_AUTOSTART:
        #     apscheduler.start()
        pass