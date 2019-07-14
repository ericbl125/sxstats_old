# monitor.py
""" is the timer that causes the update to run after the race """
from typing import List

import requests
import urllib
import re
import datetime
import sched
import time
import os
import sys


from tika import parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import location

from noaa_sdk import noaa
from location import StadiumWeather
from StatsDB import StatsDB


""" track the events for the current season """


# have a running timer
# have a running list of the current races

######################
# this section only needs to be run once a year
def get_soup(url):
    response = requests.get(url)
    html = response.text
    return BeautifulSoup(html, 'html.parser')


def get_races(year):
    soup = get_soup("https://archives.amasupercross.com/events.html")
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


#######################

#####################
# gets the dates for each race
def get_dates():
    soup = get_soup("https://www.supercrosslive.com/tickets")

    date_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5}

    dates: List[str] = []
    weeks = soup.find_all(class_='date')[2:-1]
    for week in weeks:
        date = str(week.text).strip()
        match = re.match(r'([a-z]+)([0-9]+)', date, re.I).groups()
        year = datetime.date.today().year
        date = datetime.date(year, date_dict[match[0]], int(match[1]))
        dates.append(date.isoformat())

    return dates


######################

#######################
def get_pdf(url, pdf_name):
    """ Access the pdf document from the weekly race; takes the url for the weekly race """

    # Need to perform some regualr expressions on pdf_name to make sure that the correct
    # pdf link if selected, not need to duplicate the same code that works twice

    try:
        # need to use selenium webdriver because the url is heavily javascripted
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")

        path = os.path.join(os.getcwd(), 'chromedriver')  # chromedriver is locatd within the working directory
        driver = webdriver.Chrome(path, options=chromeOptions)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # gets the pdf link, opens and parses it
        print('url %s', url)
        href_search = soup.find('a', string=re.compile(pdf_name, re.IGNORECASE))
        pdf_ref = href_search.get('href')  # soup.find('span', string=re.compile(pdf_name, re.IGNORECASE)).a.get('href')
        pdf_link = urllib.parse.urljoin(url, pdf_ref)
        pdf = parser.from_file(pdf_link)

        # return or chop the string within pdf[content]
        return pdf['content']

    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        driver.quit()


#######################

#######################
def get_location(event_link):
    # Calls the find_stadium function in Location to find the zip/long&lat of the stadium by searching
    # a wikipedia article
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")

    path = os.path.join(os.getcwd(), 'chromedriver')  # chromedriver is locatd within the working directory
    driver = webdriver.Chrome(path, options=chromeOptions)
    driver.get(event_link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    return (soup.find(id='eventtrackname').text)


def get_event_date(event_link):
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")

    path = os.path.join(os.getcwd(), 'chromedriver')  # chromedriver is locatd within the working directory
    driver = webdriver.Chrome(path, options=chromeOptions)
    driver.get(event_link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    return (soup.find(id='eventdates').text)


def get_event(event, week, year):
    """ Receives a string of event name. Opens that event from AMA archive website"""

    db = StatsDB()
    db.add_event(event, week, year)

    url = 'https://archives.amasupercross.com/'
    soup = get_soup(url)

    iframe = soup.find('iframe', id='ifrm').attrs['src']  # .find('a', string=re.compile(event))
    iframe_link = urllib.parse.urljoin(url, iframe)
    iframe_response = urllib.request.urlopen(iframe_link)
    soup = BeautifulSoup(iframe_response, 'html.parser')

    year_regex = re.compile('^' + year)
    event_ref = soup.find('a', href=year_regex, string=re.compile(event)).get('href')
    event_link = urllib.parse.urljoin(url, event_ref)

    stadium = get_location(event_link)
    event_date = get_event_date(event_link)

    race_date = datetime.datetime.strptime(event_date, '%B %d, %Y')
    start_date = race_date + datetime.timedelta(days=-1)
    end_date = race_date + datetime.timedelta(days=1)

    stadium_weather = StadiumWeather(stadium, start_date, end_date)
    weather = stadium_weather.find_stadium()

    sys.exit()

    print(event + ' AND ', week)
    entry_list = get_pdf(event_link, 'entry list').strip()
    entries = find_riders(entry_list, week, year)

    # enters the rider information into the database
    for entry in entries:
        entry = entry.split()
        number = entry[0]
        name = entry[1] + ' ' + entry[2]
        # maybe store the names found here as the regex to filter names out.
        # check if the first element is a number and then have a length requirement len(x) > 20 chars
        bike = entry[3]

        db.add_rider(name, number, bike, year)
    # call database entry for the rider

    finish_list = get_pdf(event_link, 'official results').strip()
    finishes = find_riders(finish_list[:-30], week, year)[:22]

    for index, finish in enumerate(finishes):
        # Change this to a while loop to get access to the bikes?
        finish = finish.split()
        number = finish[0]
        name = finish[1] + ' ' + finish[2]
        bike = finish[3]

        result = index + 1
        db.add_finish(event, year, name, number, bike, result)


def find_riders(pdf_list, week, year):
    pdf_list = pdf_list.splitlines()
    # regex_standings = re.compile(r'\b(?:%s)\b' % '|'.join(standings))
    # filter for start element is a number and length it greater than 15
    regex_list = re.compile('(^[1-9]).{15,}$')
    racers = list(filter(regex_list.search, pdf_list))

    return racers


####################
# Gets the Standings List for filter
####################
def get_250_standing(year):
    url = 'https://racerxonline.com/results/2019/sx/points'
    soup = get_soup("https://racerxonline.com/results/2019/sx/points")

    # Edit this for the 250'ss
    yearHref = soup.find("a", string=re.compile(year)).get("href")
    yearUrl = urllib.parse.urljoin(url, yearHref)

    response = requests.get(yearUrl)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    rows = soup.find_all("table")[1:]
    west = rows[0].find_all(itemprop='name')
    east = rows[1].find_all(itemprop='name')
    combined = west + east
    standings = []

    for row in combined:
        standings.append(row.string.lower().title())
    return standings


def get_year_standing(year):
    url = "https://racerxonline.com/results/2019/sx/points"
    soup = get_soup(url)

    yearHref = soup.find("a", string=re.compile(year)).get("href")
    yearUrl = urllib.parse.urljoin(url, yearHref)

    response = requests.get(yearUrl)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    rows = soup.find_all("table")[0].find_all(itemprop="name")
    standings = []

    for row in rows:
        standings.append(row.string.lower().title())
    return standings


def get_points_standing():
    """ Creates a list of the top ten """
    # get year and turn into string subtract 1
    year = str(int(datetime.date.today().year) - 1)

    url = 'https://racerxonline.com/results/2019/sx/points'
    soup = get_soup(url)

    rows = soup.find_all("table")[0].find_all(itemprop="name")
    standings = []

    for row in rows:
        standings.append(row.string.lower().title())
    return standings


######################
# Reload Database with Historical data
#####################

def reloadDB():
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d')
    dates = get_dates()

    db = StatsDB()
    db.clearDB()
    db.disconnect()
    # go back 4 years
    prev_year = str(int(now.year) - 3)
    while prev_year < str(now.year):
        print('Loading Year ' + prev_year)
        races = get_races(prev_year)
        for week, race in enumerate(races):
            get_event(race, week + 1, prev_year)
        prev_year = str(int(prev_year) + 1)

    print('Loading Current Season')
    races = get_races(str(now.year))
    for count, date in enumerate(dates):
        # include a check if the database needs to be refilled
        print(date)
        if date < now_str:
            get_event(races[count], count + 1, str(now.year))
        else:
            break


if __name__ == "__main__":
    ###########
    # TODO
    ##########
    # Add a logging service to keep track of each of the completed activities and any exceptions

    s = sched.scheduler(time.time, time.sleep)
    dates = get_dates()

    reloadDB()


# do I need to create a monitor class/function that runs an infinite loop to track the dates
# I need to pass parameters that will run the application
# s.enter()
