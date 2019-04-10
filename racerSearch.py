# racer search
# user selects a racer and a race to evaluate

from color import color

import requests
import urllib

from bs4 import BeautifulSoup


def getRacers():
	url = "http://www.amasupercross.com/entries.aspx?eventId=306&class=1"
	response = requests.get(url)
	html = response.text
	soup = BeautifulSoup(html, 'html.parser')

	# start finding the riders names
	rows = soup.find_all("table")[0].find_all("tr")[1:]
	riders = []
	for row in rows:
		riders.append(row.find_all("td")[1].string)
	return riders

def findTopTen():
	""" Creates a list of the top ten """
	url = "https://racerxonline.com/results/2019/sx/points"
	response = requests.get(url)
	html = response.text
	soup = BeautifulSoup(html, 'html.parser')
	
	rows = soup.find_all("table")[0].find_all(itemprop="name")[:10]
	top_ten = []
	for row in rows:
		top_ten.append(row.string)
	return top_ten



def printRiderList(riders, top_ten):
	num = 1
	for rider in riders[:30]:
		if rider in top_ten:
			print('{:>2}: {}'.format(num, color.BOLD+rider+color.END))
		else:
			print('{:>2}: {}'.format(num, rider))
		num += 1
	return riders

if __name__ == '__main__':
	""" Step 1: get a list of racers """
	racers = getRacers()
	top_ten = findTopTen()
	printRiderList(racers, top_ten)

	""" Step 2: Receive input from user """
	rider = input("Please enter # of Rider: ")
	
	# search the races for the finishes of the rider


	""" Step 3: Return the race information for the racer """









