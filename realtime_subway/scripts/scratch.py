import contextlib, urllib, requests

from datetime import datetime

from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

from realtime_subway.models import Stations


"""
API-Key in lastpass


APIs:
http://mtadatamine.s3-website-us-east-1.amazonaws.com/#/landing
https://new.mta.info/coronavirus/ridership

Routes:
    - ACE:
        - https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace

Resources:
https://medium.com/@_blahblahblah
https://github.com/neoterix/nyc-mta-arrival-notify/blob/master/mta_notification.py


API response is a General Transit Feed Specification (GTFS) which is a 
flavor of Google's protocol buffer. I think it's possible to work this 
out in vanilla python but some packages make it way easier.

https://github.com/MobilityData/gtfs-realtime-bindings
https://github.com/MobilityData/gtfs-realtime-bindings/blob/master/python/README.md
pip install --upgrade gtfs-realtime-bindings
pip install protobuf3_to_dict
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

Station ids come from a static file downloaded from here: 
http://web.mta.info/developers/developer-data-terms.html#data

In the feed the station has stop_id plus a 'N'/'S' to denote north or southbound

Ideas:
- avg route travel time


Questions:
- Can I identify a specific train car?

Data Shapes:

There can be a 'trip_update' with no 'stop_time_update'
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
    feed = gtfs_realtime_pb2.FeedMessage()

    headers = {'x-api-key': ''}
    resp = requests.get(
        'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace',
        headers=headers
    )

    feed.ParseFromString(resp.content)

    # Below is an example with data as a dict not a GTFS entity
    subway_feed = protobuf_to_dict(feed)
    print(epoch_to_utc(subway_feed.get('header').get('timestamp')))

    subway_data = subway_feed.get('entity')

    for train in subway_data:
        # unsure if ID for unique trip or ID for unique vehicle
        record_id = train.get('id')
        print(record_id)

        if 'trip_update' in train:
            print('in transit')
            
            trip_data = train.get('trip_update')
            meta_data = trip_data.get('trip')
            transit_data = trip_data.get('stop_time_update')

            print(meta_data)
            print(meta_data.get('trip_id'))
            if not transit_data:
                print('No stop_time_update')
                continue

            for stop in transit_data:
                # print(stop)
                stop_id = stop.get('stop_id')
                arr_time = stop.get('arrival').get('time')
                dep_time = stop.get('departure').get('time')

                print(f'Stop ID: {stop_id}')
                get_station_name(stop.get('stop_id'))
                
                if arr_time != dep_time:
                    print('TIME DIFFERENCE')
                    print(epoch_to_utc(arr_time))
                    print(epoch_to_utc(dep_time))
                else:
                    print(epoch_to_utc(arr_time))

        elif 'vehicle' in train:
            print('stopped')

            meta_data = train.get('vehicle')
            stop_time = train.get('stop_time_update')
            
            print(meta_data)
            print(meta_data.get('trip').get('trip_id'))

            get_station_name(meta_data.get('stop_id'))

        # import pdb; pdb.set_trace()


def get_station_name(stop_id):
    station = Stations.objects.filter(station_id=stop_id)

    if station:
        print(station[0].station_name)
    else:
        print('Station stopped at a non-existent station')


def epoch_to_utc(epoch_val):
    return datetime.utcfromtimestamp(epoch_val).strftime('%Y-%m-%d %H:%M:%S')


def run():
    ace_data()

