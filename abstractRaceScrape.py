import requests
import urllib.parse
import os
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


class abstractRaceScrape:
    def __init__(self):
        self.archive_url = 'https://archives.amasupercross.com/'
        self.soup = self.get_soup('')

    def get_soup(self, link, selenium=False):
        url = urllib.parse.urljoin(self.archive_url, link)

        if selenium:
            options = Options()
            options.headless = True

            path = os.path.join(os.getcwd(), 'geckodriver')
            driver = webdriver.Firefox(options=options, executable_path=path)
            driver.get(url)
            return BeautifulSoup(driver.page_source, 'html.parser')

        response = requests.get(url)
        html = response.text
        return BeautifulSoup(html, 'html.parser')

    def get_events(self, year):
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
