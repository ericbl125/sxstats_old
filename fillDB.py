# fillDB
""" This script runs to fill the db from scratch.  It will pull the last 5 years of racing and fill the information into the DB """
import sqlite3

url = "https://archives.amasupercross.com/events.html"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

# connect to db

