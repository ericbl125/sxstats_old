import requests
import urllib.parse
import os
import re

from sys import platform
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


class abstractRaceScrape:
    def __init__(self):
        self.archive_url = 'https://archives.amasupercross.com/'

    #TODO add error handling when getting soup to retry in different ways and manners without crashing whole program
    # TODO example would no connection
    def get_soup(self, link, selenium=False):
        url = urllib.parse.urljoin(self.archive_url, link)

        if selenium:
            options = Options()
            options.headless = True

            path = os.path.join(os.getcwd(), 'geckodriver')
            gecko = self.get_geckodriver()
            path = os.path.join(os.getcwd(), gecko)
            driver = webdriver.Firefox(options=options, executable_path=path)
            driver.get(url)
            return BeautifulSoup(driver.page_source, 'html.parser')

        response = requests.get(url)
        html = response.text
        return BeautifulSoup(html, 'html.parser')

    def get_races(self, year):
        soup = self.get_soup('')
        races = []
        weeks = soup.find_all('table')[1].find_all("tr")[1:]

        for week in weeks:
            ################
            # TODO
            ###############
            # Remove the Monster Energy Cup races
            yearRegex = re.compile('^' + year)
            races.append(week.find('a', href=yearRegex).string)

        return races[:len(races) - 1]

    @staticmethod
    def get_geckodriver():
        if platform == "linux" or platform == "linux2":
            return 'geckodriver_lin'
        elif platform == "darwin":
            return 'geckodriver_mac'
        elif platform == "win32":
            return 'geckodriver_win.exe'