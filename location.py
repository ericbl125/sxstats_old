
import requests
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
        self._wiki_url = 'https://en.wikipedia.org'
        self._geo_agent = 'sxstats'
        self._geo = Nominatim(user_agent=self._geo_agent)
        self._country_code = 'US'
        self._noaa = noaa.NOAA()

    def find_stadium(self):
        response = requests.get(self._stadium_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # [1:] drops the table header information
        table = soup.find('table').find('tbody').find_all('tr')[1:]

        for row in table:
            if re.search(self._stadium, row.a['title']):
                self.search_wiki(row.a['href'])

            # break

        # (table)

    @staticmethod
    def convert_degrees_to_decimal(lat, lon):
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

        # Conversion Formula: degrees + (minutes / 60) + (seconds / 3600)
        lat_list = lat.extract_digits()
        lat = float(lat_list[0]) + (float(lat_list[2]) / 60) + (float(lat_list[4]) / 3600)

        lon_list = lon.extract_digits()
        lon = -(float(lon_list[0]) + (float(lon_list[2]) / 60) + (float(lon_list[4]) / 3600))

        return '{}, {}'.format(round(lat, 6), round(lon, 6))

    @staticmethod
    def extract_digits(coordinate):
        return ["".join(x) for _, x in itertools.groupby(coordinate, key=str.isdigit)]

    def search_wiki(self, url_tag):
        url = self._wiki_url + url_tag
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        span = soup.find('span', title='Maps, aerial photos, and other data for this location')
        lon = str(span.find(class_='longitude').text)
        lat = str(span.find(class_='latitude').text)

        if lon and lat is None:
            location = str(span.text)
            # TODO parse into long and lat by separating them with 'N'
            location = location.extract_digits()

            print('Is None %s', location)

        coordinates = self.convert_degrees_to_decimal(lat, lon)
        location = self._geo.reverse(coordinates)
        location_dict = location.raw
        postcode = location_dict['address']['postcode']

        observations = self._noaa.get_observations(postcode, self._country_code, start=self._start_date, end=self._end_date)
        for observation in observations:
            print(observation['timestamp'])
            print(observation['precipitationLast3Hours']['value'])
            break
        print(type(observations))
