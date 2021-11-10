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

There are station_id in the feeds that aren't in station files.
"""


def ace_data():
    import_id = uuid.uuid4()

    feed = gtfs_realtime_pb2.FeedMessage()

    headers = {'x-api-key': settings.MTA_API_KEY}
    resp = requests.get(
        'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace',
        headers=headers
    )

    feed.ParseFromString(resp.content)

    for entity in feed.entity:
        print('~' * 50)
        # print(entity)
        record_id = entity.id
        print(f'record_id: {record_id}')
        # print(f'record_id: {entity.start_time}')
        # dict_entity = protobuf_to_dict(entity)
        # print(dict_entity)

        if entity.HasField('trip_update'):
            continue

            print('We are in predictive data')
            print(f'train_id: {entity.trip_update.trip.trip_id}')
            print(entity.trip_update.trip)

            for stop in entity.trip_update.stop_time_update:
                # print(stop)
                # arrival and departure are always the same time?
                print(f'{stop.arrival.time} | {epoch_to_datetime(stop.arrival.time)}')
                # print(f'{stop.departure.time} | {epoch_to_datetime(stop.departure.time)}')
                get_station_name(stop.stop_id)
                
        
        elif entity.HasField('vehicle'):
            # print('We are in current data')
            train_id = entity.vehicle.trip.trip_id.split('_')[0]
            print(f'trip_id: {entity.vehicle.trip.trip_id}')
            print(f'train_id: {train_id}')
            # print(entity.vehicle.trip)

            train_direction = 'north' if entity.vehicle.trip.trip_id.split('_')[1][-1] == 'N' else 'south'
            train_status = entity.vehicle.current_status if entity.vehicle.current_status else 2
            train_route = entity.vehicle.trip.route_id

            start_year = int(entity.vehicle.trip.start_date[0:4])
            start_month = int(entity.vehicle.trip.start_date[4:6])
            start_day = int(entity.vehicle.trip.start_date[6:])
            start_time = entity.vehicle.trip.start_time.split(':')
            start_hour = int(start_time[0])
            start_minute = int(start_time[1])
            start_second = int(start_time[2])

            start_datetime = datetime(
                start_year,
                start_month,
                start_day,
                start_hour,
                start_minute,
                start_second,
                tzinfo=pytz.UTC,
            )

            print(f'{entity.vehicle.timestamp} | {epoch_to_datetime(entity.vehicle.timestamp)}')
            update_datetime = epoch_to_datetime(entity.vehicle.timestamp)
            print(update_datetime)

            print(f'status: {entity.vehicle.current_status}')
            current_station = get_station_name(entity.vehicle.stop_id)
            print(f'Station ID: {entity.vehicle.stop_id}')

            if current_station:
                print(current_station.station_name)
                train_record = Trains(
                    record_id=record_id,
                    train_id=train_id,
                    stop_id=entity.vehicle.stop_id,
                    train_status=train_status,
                    train_direction=train_direction,
                    train_route=train_route,
                    route_start=start_datetime,
                    current_stop=current_station,
                    import_id=import_id,
                )
                train_record.save()
            else:
                print(f'Train is at station that does not exist: {entity.vehicle.stop_id}')
        
        else:
            print('How do we get here?')


def get_station_name(stop_id):
    station = Stations.objects.filter(mta_id=stop_id)

    # return station[0] if station else stop_id
    return station[0] if station else None


def epoch_to_datetime(epoch_val):
    return datetime.utcfromtimestamp(epoch_val)


def run():
    ace_data()

