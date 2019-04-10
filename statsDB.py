# Python Databse class
# this class will just need to use the function calls.
# will have two properties, the connection and the cursor (might only need the connection)
# the tables need to be directly created
# will have three tables: Riders, Races, Events

# Riders : First Name, Last Name, RiderGUID
# Races : Race Name, Week, Year, RaceGUID
# Events : Rider, Race Name, Year, Qualifing 1, Qualifying 2, Main Event, EventGUID

import psycopg2
import uuid
import datetime
import sys, os, linecache
import pytz

from config import config

class statsDB:
	
	def __init__(self):
		self.connect()
		self.add_UUID()
		self.create_tables()

	def connect(self):
		"""Connects to the database from the database.ini file."""
		params = config()
		print('Connecting to the PosgreSQL database...')
			
		self.conn = psycopg2.connect(**params)

		print('Connected to database')
		self.cur = self.conn.cursor()

	def disconnec(self):
		"""Disconnects the database from the database.ini file."""
		try:
			if self.conn is not None:
				self.conn.close()
				print('Database connection closed.')

		except (Exception, psycopg2.DatabaseError) as error:
			# PrintException()
			print(error)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)

	def create_tables(self):
		""" CREATE TABLE IF NOT EXISTS finishes (
					rider TEXT NOT NULL,
					bike TEXT NOT NULL,
					year TEXT NOT NULL,
					race01 TEXT, race02 TEXT, race03 TEXT, race04 TEXT, 
					race05 TEXT, race06 TEXT, race07 TEXT, race08 TEXT, 
					race09 TEXT, race10 TEXT, race11 TEXT, race12 TEXT, 
					race13 TEXT, race14 TEXT, race15 TEXT, race16 TEXT, 
					race17 TEXT, 
					guid UUID DEFAULT uuid_generate_v4 (),
					PRIMARY KEY (guid)
				) 
			"""


		#######################
		# TODO 
		#######################
		# Add a INPUT_DATE column to each table
		# Talbe events does not need DATE
		commands = (
			""" CREATE TABLE IF NOT EXISTS riders (
					riderID UUID DEFAULT uuid_generate_v4 (),
					name TEXT NOT NULL,
					number TEXT NOT NULL,
					bike TEXT NOT NULL,
					year TEXT NOT NULL,
					input_date TIMESTAMPTZ DEFAULT Now(),
					PRIMARY KEY (riderID)
				) 
			""",
			""" CREATE TABLE IF NOT EXISTS events (
					eventID UUID DEFAULT uuid_generate_v4 (),
					event TEXT NOT NULL,
					week TEXT NOT NULL,
					year TEXT NOT NULL,
					input_date TIMESTAMPTZ DEFAULT Now(),
					PRIMARY KEY (eventID)
				)
			""",
			""" CREATE TABLE IF NOT EXISTS finishes (
					finishID UUID DEFAULT uuid_generate_v4(),
					eventID UUID NOT NULL,
					riderID UUID NOT NULL,
					result TEXT NOT NULL,
					input_date TIMESTAMPTZ DEFAULT Now(),
					PRIMARY KEY (finishID)

				)
			"""
		)
		conn = None

		try:
			params = config()
			conn = psycopg2.connect(**params)
			cur = conn.cursor()
		
			for command in commands:
				cur.execute(command)

			conn.commit()
			cur.close()

		except (Exception, psycopg2.DatabaseError) as error:
			# self.PrintException()
			print(error)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)

		finally:
			if conn is not None:
				conn.close()
		
	def add_UUID(self):
		sql = 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
		conn = None
		try:
			params = config()
			conn = psycopg2.connect(**params)
			cur = conn.cursor()
			cur.execute(sql)

			conn.commit()
			cur.close()

		except (Exception, psycopg2.DatabaseError) as error:
			# self.PrintException()
			print(error)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)

		finally:		
			if conn is not None:
				conn.close()

	def add_rider(self, name, number, bike, year) :
		""" Checks for rider in Rider table, adds if not found """
		# generate RiderGuid
		
		# check if the rider is in the database already
		db_entry = self.find_rider(name,number,bike,year)
		# research the proper use of datetime and timezones for python and postgres
		if db_entry is None:

			sql = 'INSERT INTO riders (name, number, bike, year) VALUES(%s, %s, %s, %s)'
			conn = None
			try:
				params = config()
				conn = psycopg2.connect(**params)
				cur = conn.cursor()
				cur.execute(sql, (name, number, bike, year) )
				conn.commit()
				cur.close()

			except (Exception, psycopg2.DatabaseError) as error:
				# self.PrintException()
				print(error)
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(exc_type, fname, exc_tb.tb_lineno)

			finally:		
				if conn is not None:
					conn.close()

	def find_rider(self, name, number, bike, year):
		# run select
		sql = 'SELECT * FROM riders WHERE name=%s AND number=%s AND bike=%s AND year=%s'
		conn = None
		try:
			params = config()
			conn = psycopg2.connect(**params)
			cur = conn.cursor()
			cur.execute(sql, (name, number, bike, year))
			entry = cur.fetchone()

		except (Exception, psycopg2.DatabaseError) as error:
			# self.PrintException()
			print(error)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)

		finally:		
			if conn is not None:
				conn.close()
			return entry
		
	def add_event(self, event, week, year):
		""" Checks for the race, adds if not found """
		entry = self.find_event(event, year)
		if entry is None:
			sql = 'INSERT INTO events (event, week, year) VALUES(%s, %s, %s)'
			conn = None
			try:
				params = config()
				conn = psycopg2.connect(**params)
				cur = conn.cursor()
				cur.execute(sql, (event, week, year))
				conn.commit()
				cur.close()

			except (Exception, psycopg2.DatabaseError) as error:
				# self.PrintException()
				print(error)
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(exc_type, fname, exc_tb.tb_lineno)

			finally:		
				if conn is not None:
					conn.close()

	# Might not need this one
	def find_event(self, event, year):
		""" Receives a list containing all the information to input to the event """
		sql = 'SELECT * FROM events WHERE event=%s AND year=%s'
		# need to find the riderID
		conn = None
		
		try:
			params = config()
			conn = psycopg2.connect(**params)
			cur = conn.cursor()
			cur.execute(sql, (event, year))
			entry = cur.fetchone()

		except (Exception, psycopg2.DatabaseError) as error:
			# self.PrintException()
			print(error)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)

		finally:		
			if conn is not None:
				conn.close()
			return entry
	
	def add_finish(self, event, year, name, number, bike, result):
		""" Checks if a rider has a finishes row for a year inserts a new row if not """

		# checks for rider entry to the finishes with name and year
		# need to search for riderID and then pass it 
		conn = None
		try:
			riderID = self.find_rider(name, number, bike, year)	# returns a tuple of the entry
			if riderID is None:
				raise Exception('Event: ' + event + ' Name: ' + name + ' ' + number + ' bike: ' + bike + ' ' + year + ' Does Not Exist in riders table')
			riderID = list(riderID)[0]		# converts tuple to list because sometimes the accessing tuple return a Nonetype error even though it is type STR

			eventID = self.find_event(event, year)
			if eventID is None:
				raise TypeError('Event does not exist in events table')
			eventID = eventID[0]

			entry = self.find_finish(riderID, eventID)
			if entry is None:
				sql = 'INSERT INTO finishes (riderID, eventID, result) VALUES(%s, %s, %s)'	
				params = config()
				conn = psycopg2.connect(**params)
				cur = conn.cursor()
				cur.execute(sql, (riderID , eventID, result))
				conn.commit()
				cur.close()
				
		except (Exception, psycopg2.DatabaseError) as error:
			# self.PrintException()
			print(error)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(error)
		finally:		
			if conn is not None:
				conn.close()


	def find_finish(self, riderID, eventID):
		""" Receives a list with rider name, year, number# (week number of race) """

		# need to use eventID

		sql = 'SELECT * FROM finishes WHERE riderID=%s AND eventID=%s'
		conn = None
		
		try:
			params = config()
			conn = psycopg2.connect(**params)
			cur = conn.cursor()
			cur.execute(sql, (riderID, eventID))
			entry = cur.fetchone()

		except (Exception, psycopg2.DatabaseError) as error:
			# self.PrintException()
			print(error)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)

		finally:		
			if conn is not None:
				conn.close()
			return entry

	#################
	# dont really need this function anymore
	#################
	def update_finish(self, rider, year, raceNum, finish):
		
		# Need to verify rider season has already been entered or just have 
		race = 'race' + raceNum
		sql = 'UPDATE finishes SET ' + race + '= %s WHERE rider=%s AND year=%s'
		conn = None
		try:
			params = config()
			conn = psycopg2.connect(**params)
			cur = conn.cursor()
			cur.execute(sql, (finish, rider, year))
			conn.commit()
			cur.close()

		except (Exception, psycopg2.DatabaseError) as error:
			# self.PrintException()
			print(error)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)

		finally:		
			if conn is not None:
				conn.close()

	def search(self, sql):
		""" Runs a search based upon the given sql statement. returns the result """
		self.cur.execute(sql)
		#return the result

	def PrintException():
		exc_type, exc_obj, tb = sys.exc_info()
		f = tb.tb_frame
		lineno = tb.tb_lineno
		filename = f.f_code.co_filename
		linecache.checkcache(filename)
		line = linecache.getline(filename, lineno, f.f_globals)
		print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


