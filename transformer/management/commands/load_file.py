"""
Consolidate weather data sets to one file
"""
from django.core.management.base import BaseCommand
import pandas as pd
import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        First, create station list by combining all stations from mean, cloud, evaporation and rainfall together.
        """
        tmean_stations_file = "fixtures/temperature/tmean/HQAT_stations.txt"
        tmax_stations_file = "fixtures/temperature/tmax/HQAT_stations.txt"
        tmin_stations_file = "fixtures/temperature/tmin/HQAT_stations.txt"
        cloud_stations_file = "fixtures/cloud/HQMC_stations"
        evap_stations_file = "fixtures/evaporation/HQME_stations"
        rainfall_stations_file = "fixtures/rainfall/HQMR_stations.txt"

        with open(tmean_stations_file, 'r') as f:
            tmean_stations_contains = f.readlines()

        with open(tmax_stations_file, 'r') as f:
            tmax_stations_contains = f.readlines()

        with open(tmin_stations_file, 'r') as f:
            tmin_stations_contains = f.readlines()

        with open(cloud_stations_file, 'r') as f:
            cloud_stations_contains = f.readlines()

        with open(evap_stations_file, 'r') as f:
             evap_stations_contains = f.readlines()

        with open(rainfall_stations_file, 'r') as f:
            rainfall_stations_contains = f.readlines()

        station_list = []
        for line in tmean_stations_contains + tmax_stations_contains + tmin_stations_contains +\
                    cloud_stations_contains + evap_stations_contains + rainfall_stations_contains:
            station = {}
            values = line.strip().split(' ')
            station['station_number'] = values[0]
            station['lat'] = values[1]
            station['long'] = values[2]
            station['station_name'] = ' '.join(values[4:])
            station['country'] = 'Australia'
            station_list.append(station)

        # remove duplicate data
        station_list = [dict(t) for t in {tuple(d.items()) for d in station_list}]
        print('station_list', len(station_list))

        tmean_csv_out = "fixtures/tmean.csv"
        tmax_csv_out = "fixtures/tmax.csv"
        tmin_csv_out = "fixtures/tmin.csv"
        cloud_csv_out = "fixtures/cloud.csv"
        evap_csv_out = "fixtures/evap.csv"
        rainfall_csv_out = "fixtures/evap.csv"

        self.create_weather_csv_per_attribute(
            attribute='tmean',
            path='temperature/tmean',
            file_name='tmeanahq',
            station_list=station_list,
            csv_out=tmean_csv_out,
        )
        self.create_weather_csv_per_attribute(
            attribute='tmax',
            path='temperature/tmax',
            file_name='tmaxahq',
            station_list=station_list,
            csv_out=tmax_csv_out,
        )
        self.create_weather_csv_per_attribute(
            attribute='tmin',
            path='temperature/tmin',
            file_name='tminahq',
            station_list=station_list,
            csv_out=tmin_csv_out,
        )
        self.create_weather_csv_per_attribute(
            attribute='cloud',
            path='cloud',
            file_name='cldmhq',
            station_list=station_list,
            csv_out=cloud_csv_out,
        )
        self.create_weather_csv_per_attribute(
            attribute='evaporation',
            path='evaporation',
            file_name='evaphq',
            station_list=station_list,
            csv_out=evap_csv_out,
        )
        self.create_weather_csv_per_attribute(
            attribute='rainfall',
            path='rainfall',
            file_name='prcphq',
            station_list=station_list,
            csv_out=rainfall_csv_out,
        )

        # using pandas to merge files
        tmean_file = pd.read_csv(tmean_csv_out)
        tmax_file = pd.read_csv(tmax_csv_out)
        tmin_file = pd.read_csv(tmin_csv_out)
        cloud_file = pd.read_csv(tmin_csv_out)
        evap_file = pd.read_csv(tmin_csv_out)
        rainfall_file = pd.read_csv(rainfall_csv_out)

        merge_columns = ['station_number', 'lat', 'long', 'station_name', 'country', 'year']
        result = pd.merge(tmean_file, tmax_file, how='outer', on=merge_columns)
        result = pd.merge(result, tmin_file, how='outer', on=merge_columns)
        result = pd.merge(result, cloud_file, how='outer', on=merge_columns)
        result = pd.merge(result, evap_file, how='outer', on=merge_columns)
        result = pd.merge(result, rainfall_file, how='outer', on=merge_columns)
        # TODO: refactor using concat
        # columns = ['station_number', 'lat', 'long', 'station_name', 'country', 'year', 'tmean', 'tmax']
        # result = pd.concat(
        #     objs=[tmean_file, tmax_file],
        #     axis=1,
        #     join='outer',
        # )
        result.to_csv('fixtures/weather.csv')

    @staticmethod
    def create_weather_csv_per_attribute(attribute, path, file_name, station_list, csv_out):
        records = []
        for station in station_list:
            station_file = "fixtures/{}/{}.{}.annual.txt".format(path, file_name, station['station_number'])
            try:
                with open(station_file, 'r') as f:
                    # ignore the first line
                    next(f)
                    station_contain = f.readlines()
                for l in station_contain:
                    row = {}
                    row['station_number'] = station['station_number']
                    row['lat'] = station['lat']
                    row['long'] = station['long']
                    row['station_name'] = station['station_name']
                    row['country'] = station['country']
                    values = l.strip().split()
                    row['year'] = values[0][:4]
                    row[attribute] = values[2]
                    records.append(row)
            except FileNotFoundError:
                print('cannot find %s value of %s station' % (attribute, station['station_number']))
                pass
        print('%s %s records have been founded' % (len(records), attribute))
        with open(csv_out, 'w') as fw:
            writer = csv.DictWriter(fw, fieldnames=row)
            writer.writeheader()
            writer.writerows(records)
