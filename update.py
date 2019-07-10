#update.py
""" This updates the database with the newest race information """
import requests
import urllib
import re
import datetime

from bs4 import BeautifulSoup

# this is the url for the most current supercros race
def track

def getQualifying():



url = "https://archives.amasupercross.com/events.html"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')



list = soup.find_all(string=re.compile(self.event))


