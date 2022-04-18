import csv
import requests
from datetime import date
from operator import itemgetter
from bs4 import BeautifulSoup

# from realtime_subway.models import Fares

"""
MTA New York City Transit posts the latest data every Saturday by 1 a.m.

"""

class FareDataScraper:
    def __init__(self):
        self.base_url = 'http://web.mta.info/developers/'
        self.fare_types = self.get_fare_types()
        # list of tuples (ie date & url)
        # or dict of date: url
        self.fare_data_urls = []
        self.fare_data = []
        self.sorted_stations = []

    def get_fare_types(self):
        """
        This file does not have all the fare types that appear in fare files.

        TODO: Headers have changed over the years. Will need to find all variations and normalize them.
        """
        # This url is on the fare.html page. If it starts to move we can grab it from their instead of hardcoding
        # resp = requests.get(self.base_url + 'resources/nyct/fares/fare_type_description.txt')

        # # First two lines are useless for our purpsoses
        # for line in resp.text.splitlines()[2:]:
        #     fare_types = line.split('=')
        #     self.fare_types[fare_types[0].strip()] = fare_types[1].strip()

        return {
            'FF': 'Full Fare',
            'SEN/DIS': 'Senior Citizen/Disabled',
            ' 7-D AFAS UNL': '7 Day ADA Unlimited',
            '30-D AFAS/RMF UNL': '30 Day ADA/RFM Unlimited',
            'JOINT RR TKT': 'Joint Rail Road Ticket',
            '7-D UNL': '7 Day Unlimited',
            '30-D UNL': '30 Day Unlimited',
            '7D-XBUS PASS': '7 Day Express Bus Pass',
            'TCMC': 'Transit Check MetroCard',
            'RF 2 TRIP': 'Reduced Fair 2 Trip',
            'RR UNL NO TRADE': 'Rail Road Unlimited No Trade',
            'TCMC ANNUAL MC': 'Transit Check MetroCard Annual MetroCard',
            'MR EZPAY EXP': 'Mail and Ride EzPay Express',
            'MR EZPAY UNL': 'Mail and Ride EzPay Unlimited',
            'PATH 2-T': 'PATH 2 Trip',
            'AIRTRAIN FF': 'AirTrain Full Fare',
            'AIRTRAIN 30-D': 'AirTrain 30 Day',
            'AIRTRAIN 10-T': 'AirTrain 10 Trip',
            'AIRTRAIN MTHLY': 'AirTrain Monthly',
            'STUDENTS': 'Student Usage',
            'NICE 2-T': 'Nassau Inter-County Express 2 Trip',
            'CUNY-120': 'CUNY 120 Day',
            'CUNY-60': 'CUNY 60 Day',
            'FF VALUE': 'Full Fare Value',
            'FF 7-DAY': 'Full Fare 7 Day',
            'FF 30-DAY': 'Full Fare 30 Day'
        }


    def get_fare_files(self):
        # fare.html gives us the page with all available urls we can fetch
        resp = requests.get(self.base_url + 'fare.html')

        parsed_resp = BeautifulSoup(resp.text, 'html.parser')
        # NOTE: Not sure how consistent this selector is
        # A .find() gives us a single ResultSet containing all data set anchor tags
        fare_data_div = parsed_resp.find("div", {"class": "last"})

        # Loop over each anchor tag and get the specific dataset url
        for data_elem in fare_data_div.find_all('a'):
            # TODO contruct an actual date var using the end of the url (ie 110305)
            data_date = data_elem.text
            data_url = self.base_url + data_elem.attrs['href']

            self.fare_data_urls.append((data_date, data_url))


    def parse_latest_fare_file(self):
        fetch_url = self.fare_data_urls[0][1]
        # print(fetch_url)

        # http://web.mta.info/developers/data/nyct/fares/fares_220129.csv
        resp = requests.get(fetch_url)

        # This is messy. The date in the URL is from the upload date NOT the date of the data.
        # The second line has the start/end dates in it and lots of empty columns and hyphenated start/end. 
        data_date = resp.text.splitlines()[1].split(',')[1].split('-')
        data_start = data_date[0].split('/')
        data_end = data_date[1].split('/')
        data_upload = fetch_url.split('_')[1].split('.')[0]

        data_start_date = date(year=int(data_start[2]), month=int(data_start[0]), day=int(data_start[1]))
        data_end_date = date(year=int(data_end[2]), month=int(data_end[0]), day=int(data_end[1]))
        data_upload_date = date(year=int(f'20{data_upload[0:2]}'), month=int(data_upload[2:4]), day=int(data_upload[4:]))

        print(f'{data_start_date} | {data_end_date}')

        # First two lines are useless for our purposes. Skipping them gives us an easier DictReader
        fare_reader = csv.DictReader(resp.text.splitlines()[2:], delimiter=',')

        # TODO: Update to be a dictionary of all total values.
        # Second dictioary for called stations
        # Add remote ID
        fare_data = {
            'dates': {
                'start_date': data_start_date.strftime('%d/%m/%Y'),
                'end_date': data_end_date.strftime('%d/%m/%Y'),
            },
            'totals': {
                'swipes': 0
            },
            'stations': {},
        }

        for val in self.fare_types.values():
            fare_data['totals'][val] = 0

        for line in fare_reader:
            total_swipes = 0

            station = line.get(' STATION').strip(' ').title()
            station_id = line.get('REMOTE').strip(' ')

            fare_data['stations'][station] = {}
            fare_data['stations'][station]['Remote ID'] = station_id
            print(line)
            print('~~~~~~~~~~ ' + station + ' ~~~~~~~~~~')

            for key, val in self.fare_types.items():
                swipes = int(line.get(key))
                fare_data['stations'][station].update({val: swipes})
                
                # fare_data['total_' + '_'.join(val.lower().split())] += swipes
                fare_data['totals'][val] += swipes
                total_swipes += swipes

            fare_data['stations'][station]['total_swipes'] = total_swipes
            fare_data['totals']['swipes'] += total_swipes
            self.sorted_stations.append((station, total_swipes))

            # print(f'Total Swipes: {total_swipes}')
            # print('Detailed Breakdown: ')
            # print(fare_data['stations'][station])

        # print(fare_data)
        self.sorted_stations.sort(key=itemgetter(1), reverse=True)
        self.fare_data.append(fare_data)


    # def get_fare_files(self):
    #     print(self.fare_data_urls)
    #     fetch_url = self.fare_data_urls[0][1]
    #     # print(fetch_url)

    #     # http://web.mta.info/developers/data/nyct/fares/fares_220129.csv
    #     resp = requests.get(fetch_url)

    #     # This is messy. The date in the URL is from the upload date NOT the date of the data.
    #     # The second line has the start/end dates in it and lots of empty columns and hyphenated start/end. 
    #     data_date = resp.text.splitlines()[1].split(',')[1].split('-')
    #     data_start = data_date[0].split('/')
    #     data_end = data_date[1].split('/')
    #     data_upload = fetch_url.split('_')[1].split('.')[0]

    #     data_start_date = date(year=int(data_start[2]), month=int(data_start[0]), day=int(data_start[1]))
    #     data_end_date = date(year=int(data_end[2]), month=int(data_end[0]), day=int(data_end[1]))
    #     data_upload_date = date(year=int(f'20{data_upload[0:2]}'), month=int(data_upload[2:4]), day=int(data_upload[4:]))

    #     print(f'Uploaded on: {data_upload_date}')
    #     print(f'{data_start_date} | {data_end_date}')

    #     # First two lines are useless for our purposes. Skipping them gives us an easier DictReader
    #     fare_reader = csv.DictReader(resp.text.splitlines()[2:], delimiter=',')

    #     for line in fare_reader:
    #         station_data = []

    #         total_swipes = 0

    #         station = line.get(' STATION').strip(' ').title()
    #         station_id = line.get('REMOTE').strip(' ')

    #         print(line)
    #         print('~~~~~~~~~~ ' + station + ' ~~~~~~~~~~')

    #         for key, val in self.fare_types.items():
    #             swipes = int(line.get(key))

    #             # TODO add uuid4 instead of an autoincrementer
    #             fare_row = {
    #                 'datetime_fare_started': data_start_date,
    #                 'datetime_fare_ended': data_end_date,
    #                 'datetime_uploaded': data_upload_date,
    #                 # NOTE this can be ommited b/c of DB auto value
    #                 'datetime_imported': '',
    #                 'fare_swipe_type': val,
    #                 'station_remote_id': station_id,
    #                 'station_name': station,
    #                 'swipes': swipes,
    #             }

    #             # db_row = Fares(**fare_row)
    #             # station_data.append(db_row)

    #         # TODO play around with where this actually executes
    #         # Fares.objects.bulk_create(station_data)

    #         self.sorted_stations.append((station, total_swipes))


    def get_busiest_stations(self):
        print(f'{self.sorted_stations}')
        print(f'The busiest station this week was {self.sorted_stations[0][0]} with {self.sorted_stations[0][1]} swipes')
        return self.sorted_stations[0]


# def run():
#     fare_scraper = FareDataScraper()
#     fare_scraper.get_fare_files()
#     fare_scraper.get_fare_files()
#     fare_scraper.get_busiest_stations()


if __name__ == '__main__':
    fare_scraper = FareDataScraper()
    fare_scraper.get_fare_files()
    fare_scraper.parse_latest_fare_file()
    fare_scraper.get_busiest_stations()
