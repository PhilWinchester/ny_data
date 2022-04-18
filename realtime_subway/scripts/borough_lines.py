import csv
from operator import delitem

# Path is from ny_data root
DETAILED_STATIONS = 'realtime_subway/fixtures/stations.csv'


BOROUGH_MAP = {
    'M': 'Manhattan',
    'Q': 'Queens',
    'Bk': 'Brooklyn',
    'Bx': 'Bronx',
    'SI': 'Staten Island',
}


class StationImporter:
    def __init__(self):
        self.borough_dict = {}
        self.subway_lines = set()
        self.line_map = {}


    def get_fixture_data(self):
        with open(DETAILED_STATIONS, 'r') as stations_file:
            stations_csv = csv.DictReader(stations_file, delimiter=',')

            for line in stations_csv:
                borough = BOROUGH_MAP.get(line.get('Borough'))
                routes = line.get('Daytime Routes').split(' ')

                # populate our dictionary of all boroughs and the 
                # subway lines that run through them
                if borough in self.borough_dict:
                    for route in routes:
                        self.borough_dict[borough].add(route)
                else:
                    # Declaring a set explicitly with set('abc') will give us {'a','b','c'}
                    # This syntax won't pull apart the string and gives us our single value
                    self.borough_dict[borough] = {routes[0]}
                    
                    for route in routes[1:]:
                        self.borough_dict[borough].add(route)

                # populate our set of unique subway lines
                for route in routes:
                    if route not in self.subway_lines:
                        self.subway_lines.add(route)

    def get_overlap_lines(self):
        for line in self.subway_lines:
            self.line_map[line] = set()

            for borough in self.borough_dict:
                if line in self.borough_dict[borough]:
                    self.line_map[line].add(borough)

    def get_most_crosses(self):
        """
            Find the subway line that goes through the most boroughs
        """
        most_boroughs = 0

        for line in self.line_map:
            # print(f'{line}: {len(self.line_map[line])}')

            num_boroughs = len(self.line_map[line])

            if num_boroughs > most_boroughs:
                line_names = [line]
                most_boroughs = num_boroughs

            elif num_boroughs == most_boroughs:
                line_names.append(line)

        print(f'There are {len(line_names)} line(s) that appear in {most_boroughs} boroughs. The lines are: ')
        print(line_names)




def run():
    station_import = StationImporter()
    
    station_import.get_fixture_data()
    print(station_import.borough_dict)
    print(station_import.subway_lines)
    
    station_import.get_overlap_lines()
    print(station_import.line_map)

    station_import.get_most_crosses()


if __name__ == '__main__':
    run()
