import requests
import pytz
import uuid

from datetime import datetime, tzinfo

from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
from django.conf import settings

from realtime_subway.models import Stations, Trains


"""
API-Key in lastpass

API response is a General Transit Feed Specification (GTFS) which is a 
flavor of Google's protocol buffer.

Ideas:
- avg route travel time

Questions:
- Can I identify a specific train car?
- Why do certain train_ids appear 3 times?

Data Shapes:
Each trip_id appears twice. First time is the first shape below (ie 'trip_update' contains predicted arrivals)
    and the second time is the second shape (ie 'vehicle' has current stop & status).
{
    'id': '000001A', 
    'trip_update': {
        'trip': {
            'trip_id': '060790_A..S', 
            'start_time': '10:07:54', 
            'start_date': '20211103', 
            'route_id': 'A'
        }, 
        'stop_time_update': [{
            'arrival': {'time': 1635954238}, 
            'departure': {'time': 1635954238}, 
            'stop_id': 'H12S'
        }, {
            'arrival': {'time': 1635954328}, 
            'departure': {'time': 1635954328}, 
            'stop_id': 'H13S'
        }, {
            'arrival': {'time': 1635954388}, 
            'departure': {'time': 1635954388}, 
            'stop_id': 'H14S'
        }, {
            'arrival': {'time': 1635954478},
            'departure': {'time': 1635954478}, 
            'stop_id': 'H15S'
        }]
    }
}
{
    'id': '000010A', 
    'vehicle': {
        'trip': {
            'trip_id': '062846_A..S',
            'start_time': '10:28:28',
            'start_date': '20211103',
            'route_id': 'A'
        }, 
        'current_stop_sequence': 29, 
        'current_status': 1, 
        'timestamp': 1635954352,
        'stop_id': 'A63S'
    }
}

station = Stations.objects.filter(station_id='A63S')
station.values().first().get('station_name')

OR

station = Stations.objects.filter(station_id='A63S')[0]
station.station_name

NOTE
There are station_id in the feeds that aren't in station files.

TODO
Make sure all timezones are in EST.
    - vehicle.trip starttime = EST
    - trip_update.trip starttime = EST
    - vehicle.timestamp = UTC?
    - trip_update.stop_time_update = UTC?
Trip Status is flipped? in their feed/how I parse it
"""


# TODO: Add logging of full merged "record" for easier debugging
def ace_data():
    import_id = uuid.uuid4()

    feed = gtfs_realtime_pb2.FeedMessage()

    headers = {'x-api-key': settings.MTA_API_KEY}
    resp = requests.get(
        'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace',
        headers=headers
    )

    feed.ParseFromString(resp.content)

    trip_data = {}

    for entity in feed.entity:
        """
        Map the two fields into one object. 
        The "raw" version goes into a log table/topic
        A formatted version (here or in a consumer) goes into some sort of stops/trains table.
            That table is what let's us know where a train is on it's route.
        """
        # print('~' * 50)
        record_id = entity.id

        if entity.HasField('trip_update'):
            if not trip_data:
                trip_data = {
                    'record_id': record_id,
                    'import_id': import_id,
                    'train_id': entity.trip_update.trip.trip_id,
                    'train_route': entity.trip_update.trip.route_id,
                    'train_direction': 'north' if entity.trip_update.trip.trip_id[-1] == 'N' else 'south',
                    # Looks like route start is local time (ET) not UTC
                    'route_start': get_trip_starttime(entity.trip_update),
                }

                stop_data = [stop for stop in entity.trip_update.stop_time_update]

                # print(stop_data)
                if len(stop_data) > 1:
                    # stop_data[0] is always current stop if either stopped at or in transit to next
                    trip_data.update({
                        'next_stop': get_station_name(stop_data[1].stop_id),
                        # TODO figure out timezone
                        'estimated_time': epoch_to_datetime(stop_data[1].arrival.time)
                    })
                
        
        elif entity.HasField('vehicle') and trip_data:
            if trip_data and trip_data.get('train_id') == entity.vehicle.trip.trip_id:
                """
                At this point we should know the route, starttime & date, and next stop(s).
                We can find current time, current stop, current status, and stop sequence (useful?)
                """
                # print(entity.vehicle)
                # print(entity.vehicle.current_status)
                
                # TODO: If train is active (ie current_status = 1)
                #  Look for last import value and compare train station
                #  If stations is different calculate the time diff (it's gonna be 30 seconds)

                trip_data.update({
                    'stop_id': entity.vehicle.stop_id,
                    'current_stop': get_station_name(entity.vehicle.stop_id),
                    # This logic is flipped? 
                    # If no current_status the train hasn't started/has finished it's route
                    'train_status': entity.vehicle.current_status if entity.vehicle.current_status else 2,
                })

            else:
                print('mismatching train_ids')
                trip_data = {}

            train_record = Trains(**trip_data)
            train_record.save()

            trip_data = {}


def get_trip_starttime(trip_update):
    start_year = int(trip_update.trip.start_date[0:4])
    start_month = int(trip_update.trip.start_date[4:6])
    start_day = int(trip_update.trip.start_date[6:])
    start_time = trip_update.trip.start_time.split(':')
    start_hour = int(start_time[0])
    start_minute = int(start_time[1])
    start_second = int(start_time[2])

    return datetime(
        start_year,
        start_month,
        start_day,
        start_hour,
        start_minute,
        start_second,
        tzinfo=pytz.timezone('US/Eastern'),
    )


def get_station_name(stop_id):
    station = Stations.objects.filter(mta_id=stop_id)

    # return station[0] if station else stop_id
    return station[0] if station else None


def epoch_to_datetime(epoch_val):
    return datetime.utcfromtimestamp(epoch_val).astimezone(tz=pytz.timezone('US/Eastern'))


def run():
    ace_data()

