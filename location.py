# Add the location (coordinates or zip code) for each stadium to a local/db doc/table

import requests
import urllib
import re
import itertools

from geopy.geocoders import Nominatim
from noaa_sdk import noaa

from bs4 import BeautifulSoup

#################
# TODO Convert this into a class. Named 'Stadium_Weather'
# Class will have a main method that receives a date range and stadium name.
#   Main method will be get_weather? find_stadium? or retrieve?
#   This method will be the sole interaction with the callee with all other methods being private
################


class StadiumWeather:

    def _init_(self, stadium, start_date, end_date):
        self._stadium = stadium
        self._start_date = start_date
        self._end_date = end_date

        self._stadium_url = 'https://en.wikipedia.org/wiki/List_of_U.S._stadiums_by_capacity'
        self._geo_agent = "sxstats"
        self._geo = Nominatim(user_agent=self._geo_agent)
        self._noaa = noaa.NOAA()

    def find_stadium(self, stadium):
        response = requests.get(self._stadium_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # [1:] drops the table header information
        table = soup.find('table').find('tbody').find_all('tr')[1:]

        for row in table:
            if re.search(stadium, row.a['title']):
                self.search_wiki(row.a['href'])

            # break

        # (table)


    def convert_degrees_to_decimal(self, lat, lon):
        """Converts latitude and longitude from degrees to decimal

            Just a simple function to convert to decimal which is used on observations

        Args:
            lat (str): latitude
            lon (str): longitude
        Returns:
            (lat, lon)
            """
        # separate by non numbers
        # 32°44′52″N
        # 97°5′34″W

        lat_list = ["".join(x) for _, x in itertools.groupby(lat, key=str.isdigit)]
        lat = float(lat_list[0]) + (float(lat_list[2]) / 60) + (float(lat_list[4]) / 3600)

        lon_list = ["".join(x) for _, x in itertools.groupby(lon, key=str.isdigit)]
        lon = -(float(lon_list[0]) + (float(lon_list[2]) / 60) + (float(lon_list[4]) / 3600))

        return '{}, {}'.format(round(lat, 6), round(lon, 6))

    def search_wiki(self, url_tag):
        url = 'https://en.wikipedia.org' + url_tag
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # geolocator = Nominatim(user_agent='sxstats')

        span = soup.find('span', title='Maps, aerial photos, and other data for this location')
        lon = str(span.find(class_='longitude').text)
        lat = str(span.find(class_='latitude').text)

        # Use the long and lat by calling noaa.points_forecast
        if lon and lat is None:
            location = str(span.text)
            # parse into long and lat by separating them with 'N'
            print('Is None %s', location)
        else:
            coordinates = self.convert_degrees_to_decimal(lat, lon)
            location = self._geo.reverse(coordinates)

            # observations = n.points_observations(lat, long, start='2017-01-01', end='2018-02-02')
            # for observation in observations:
            #    print(observation)
        location_dict = location.raw
        postcode = location_dict['address']['postcode']

        # n = noaa.NOAA()
        observations = self._noaa.get_observations(postcode, 'US', start='2017-01-01', end='2018-02-02')
        for observation in observations:
            print(observation['timestamp'])
            print(observation['precipitationLast3Hours']['value'])
            break
        print((type(observations)))