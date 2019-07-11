import requests
import urllib.parse
import re
import datetime
import sched
import time
import os
import sys

import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from abstractRaceScrape import abstractRaceScrape


class YearlyLoad(abstractRaceScrape):

    def __init__(self, year=None):
        self.year = year
        if self.year is None:
            self.year = str(datetime.datetime.now().year)
        abstractRaceScrape.__init__(self)

    def get_location(self, event_link):
        soup = self.get_soup(event_link, selenium=True)
        return soup.find(id='eventtrackname').text

    def get_race_date(self, event_link):
        soup = self.get_soup(event_link, selenium=True)
        return soup.find(id='eventdates').text

    def main(self):
        iframe_src = self.soup.find('iframe', id='ifrm').attrs['src']
        soup_iframe = self.get_soup(iframe_src)

        weeks = soup_iframe.find_all('table')[1].find_all("tr")[1:]
        for week in weeks:
            year_regex = re.compile('^' + self.year)
            stadium = self.get_location(week.find('a', href=year_regex).get('href'))

            # TODO grab date for event
            # TODO get coordinates for event from wikipedia
            # TODO get postcode for event
            # TODO store data into DB
            time.sleep(5)


yl = YearlyLoad('2019')
yl.main()

