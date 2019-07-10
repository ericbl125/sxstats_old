import requests
import urllib.parse
import re
import datetime
import sched
import time
import os
import sys

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
        races = self.get_races(self.year)

