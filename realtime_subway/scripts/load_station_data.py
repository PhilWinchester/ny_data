"""
Station ids come from a static file downloaded from here: 
http://web.mta.info/developers/developer-data-terms.html#data

TODO:
    Records with no data are not being correctly inserted as NULL values.
    (ie northbound_desc/southbound_desc are empty strings not NULL)
"""
import csv

from realtime_subway.models import Stations

# Path is from ny_data root
DIRECTION_STATIONS = 'realtime_subway/fixtures/stops.txt'
DETAILED_STATIONS = 'realtime_subway/fixtures/stations.csv'


BOROUGH_MAP = {
    'M': 'Manhattan',
    'Q': 'Queens',
    'Bk': 'Brooklyn',
    'Bx': 'Bronx',
    'SI': 'Staten Island',
}


def open_files():

    stations_dict = {}

    with open(DIRECTION_STATIONS, 'r') as station_csv:
        """
            This CSV has 3 rows for each station. One as the "overall",
            one as "northbound", and one as "southbound." 
        """
        station_file = csv.DictReader(station_csv, delimiter=',')

        for station in station_file:
            stations_dict[station.get('stop_id')] = {
                'station_latitude': station.get('stop_lat'),
                'station_longitude': station.get('stop_lon'),
                'station_parent_id': station.get('parent_station'),
            }

    with open(DETAILED_STATIONS, 'r') as detailed_csv:
        """
            This CSV has one row for each station. Need to map the information
            into the 3 copies of each station in the dictionary.

            Station ID, Complex ID, GTFS Stop ID, Division
            , Line, Stop Name, Borough, Daytime Routes, Structure
            , GTFS Latitude, GTFS Longitude, North Direction Label
            , South Direction Label, ADA, ADA Notes
        """
        station_file = csv.DictReader(detailed_csv, delimiter=',')

        for station in station_file:
            station_id = station.get('GTFS Stop ID')
            south_id = f'{station_id}S'
            north_id = f'{station_id}N'

            borough = BOROUGH_MAP[station.get('Borough')]
            # concat station name + lines for unique name?
            station_name = station.get('Stop Name')
            station_lines = ','.join(station.get('Daytime Routes').split(' '))
            is_elevated = station.get('Structure') == 'Elevated'

            if stations_dict.get(station_id):
                stations_dict[station_id].update({
                    'mta_id': station_id,
                    'station_borough': borough,
                    'station_name': station_name,
                    'station_lines': station_lines,
                    'station_elevated': is_elevated,
                })
                parent_station = Stations(**stations_dict[station_id])
                parent_station.save()

            if stations_dict.get(south_id):
                south_label = station.get('South Direction Label')

                stations_dict[south_id].update({
                    'mta_id': south_id,
                    'station_borough': borough,
                    'station_name': station_name,
                    'station_lines': station_lines,
                    'station_elevated': is_elevated,
                    'southbound_desc': south_label,
                })
                south_station = Stations(**stations_dict[south_id])
                south_station.save()

            if stations_dict.get(north_id):
                north_label = station.get('North Direction Label')

                stations_dict[north_id].update({
                    'mta_id': north_id,
                    'station_borough': borough,
                    'station_name': station_name,
                    'station_lines': station_lines,
                    'station_elevated': is_elevated,
                    'northbound_desc': north_label,
                })

                north_station = Stations(**stations_dict[north_id])
                north_station.save()


def run():
    # TODO is this check necessary?
    stations = Stations.objects.all()
    if not stations:
        open_files()
    else:
        print('Station Data already loaded')
