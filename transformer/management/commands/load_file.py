"""
Consolidate weather data sets to one file
"""
# from halo import Halo
#
# class Transformer:
#     def load(self):
#         """Load all the files here"""
#         return
#
#     def load_station(self):
#         """Load 5 stations files and put them into 1 file"""
#         self.cloud_stations = '../fixtures/cloud/HQMC_stations'
#         self.source_cloude_stations = open(self.cloud_stations, encoding='iso8859-1')
#         self.spinner = Halo(
#             text="Loading cloud stations",
#             spinner='dots',
#         )

from django.core.management.base import BaseCommand
import csv


class Command(BaseCommand):

    def handle(self, *args, **options):
        mean_temp_file = "fixtures/temperature/tmean/HQAT_stations.txt"
        cloud_file = "fixtures/cloud/HQMC_stations"
        evaporation_file = "fixtures/evaporation/HQME_stations"
        rainfall_file = "fixtures/rainfall/HQMR_stations.txt"
        csv_file = "fixtures/weather.csv"
        records = []

        with open(mean_temp_file, 'r') as f:
            contents_f1 = f.readlines()

        with open(cloud_file, 'r') as f:
            contents_f2 = f.readlines()

        with open(evaporation_file, 'r') as f:
            contents_f3 = f.readlines()

        with open(rainfall_file, 'r') as f:
            contents_f4 = f.readlines()

        for line in contents_f1:
            row = {}
            values = line.strip().split(' ')
            tmean_station_file = "fixtures/temperature/tmax/tmaxahq.{}.annual.txt".format(values[0])
            row['station_number'] = values[0]
            row['latitude'] = values[1]
            row['longitude'] = values[2]
            row['station_name'] = ' '.join(values[4:])
            row['country'] = 'Australia'
            try:
                with open(tmean_station_file, 'r') as f:
                    contain = f.readlines()
                    index = 1
                    for l in contain:
                        tmean_values = l.strip().split(' ')
                        row['year'] = tmean_values[0]
                        # print(tmean_values[0].index())
                        row['tmean'] = tmean_values[2]
                        index = index + 1
                        records.append(row)
                        print(row)
            except FileNotFoundError:
                pass

        with open(csv_file, 'w') as fw:
            writer = csv.DictWriter(fw, fieldnames=row)
            writer.writeheader()
            writer.writerows(records)
