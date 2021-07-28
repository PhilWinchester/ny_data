import re
import json
import requests

from datetime import datetime

from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict


"""
API-Key: 


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

"""

def ace_data():
    feed = gtfs_realtime_pb2.FeedMessage()

    headers = {'x-api-key': '2yIFQSFD13NV1t44UKqw3HWFxFEkK53hW1z4Hdf0'}
    resp = requests.get(
        'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace',
        headers=headers
    )

    feed.ParseFromString(resp.content)

    subway_feed = protobuf_to_dict(feed)
    subway_data = subway_feed.get('entity')

    for train in subway_data:
        print(train.id)

        if train.HasField('trip_update'):
            print('in transit')
            print(train.trip_update.stop_time_update)
            datetime.utcfromtimestamp(
                train.trip_update.stop_time_update[0].arrival.time
            ).strftime('%Y-%m-%d %H:%M:%S')
        elif train.HasField('vehicle'):
            print('stopped')

        # print(train)

def epoch_to_utc(epoch_val):
    return datetime.utcfromtimestamp(epoch_val).strftime('%Y-%m-%d %H:%M:%S')

for stop in feed.entity[2].trip_update.stop_time_update:
    print(f'''
    {stop.stop_id}: 
        - Arrival = {epoch_to_utc(stop.arrival.time)}
        - Departure = {epoch_to_utc(stop.departure.time)}
    ''')

if __name__ == '__main__':
    ace_data()

