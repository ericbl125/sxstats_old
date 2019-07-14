# Python Databse class
# this class will just need to use the function calls.
# will have two properties, the connection and the cursor (might only need the connection)
# the tables need to be directly created
# will have three tables: Riders, Races, Events

# Riders : First Name, Last Name, RiderGUID
# Races : Race Name, Week, Year, RaceGUID
# Events : Rider, Race Name, Year, Qualifing 1, Qualifying 2, Main Event, EventGUID

import psycopg2
import sys
import os

from config import config


class StatsDB:

    def __init__(self):
        self.connect()
        self.add_UUID()
        self.create_tables()

    @staticmethod
    def connect():
        """Connects to the database from the database.ini file."""
        params = config()
        print('Connecting to the PosgreSQL database...')

        conn = psycopg2.connect(**params)
        print('Connected to database')

    @staticmethod
    def disconnect():
        """Disconnects the database from the database.ini file."""
        conn = None
        try:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    @staticmethod
    def create_tables():
        #######################
        # TODO add a weather Table to track all the weather information; join on by event_id
        #######################
        # TODO Add a INPUT_DATE column to each table
        commands = (
            """ CREATE TABLE IF NOT EXISTS riders (
                    rider_id UUID DEFAULT uuid_generate_v4 (),
                    name TEXT NOT NULL,
                    number TEXT NOT NULL,
                    bike TEXT NOT NULL,
                    year TEXT NOT NULL,
                    input_date TIMESTAMPTZ DEFAULT Now(),
                    PRIMARY KEY (rider_id)
                ) 
            """,
            """ CREATE TABLE IF NOT EXISTS events (
                    event_id UUID DEFAULT uuid_generate_v4 (),
                    event TEXT NOT NULL,
                    week TEXT NOT NULL,
                    year TEXT NOT NULL,
                    input_date TIMESTAMPTZ DEFAULT Now(),
                    PRIMARY KEY (event_id)
                )
            """,
            """ CREATE TABLE IF NOT EXISTS finishes (
                    finish_id UUID DEFAULT uuid_generate_v4(),
                    event_id UUID NOT NULL,
                    rider_id UUID NOT NULL,
                    result TEXT NOT NULL,
                    input_date TIMESTAMPTZ DEFAULT Now(),
                    PRIMARY KEY (finish_id)

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
            print(error)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def add_UUID():
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
            print(error)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def clearDB():
        print('Truncating Tables')
        sql = 'TRUNCATE riders; ' + 'TRUNCATE events; ' + 'TRUNCATE finishes;'
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        finally:
            if conn is not None:
                conn.close()

    def add_rider(self, name, number, bike, year):
        """ Checks for rider in Rider table, adds if not found """
        # generate RiderGuid

        # check if the rider is in the database already
        db_entry = self.find_rider(name, number, bike, year)
        # research the proper use of datetime and timezones for python and postgres
        if db_entry is None:

            sql = 'INSERT INTO riders (name, number, bike, year) VALUES(%s, %s, %s, %s)'
            conn = None
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(sql, (name, number, bike, year))
                conn.commit()
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

            finally:
                if conn is not None:
                    conn.close()

    @staticmethod
    def find_rider(name, number, bike, year):
        # run select
        sql = 'SELECT * FROM riders WHERE name=%s AND number=%s AND bike=%s AND year=%s'
        conn = None
        entry = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (name, number, bike, year))
            entry = cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
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
                print(error)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

            finally:
                if conn is not None:
                    conn.close()

    # Might not need this one
    @staticmethod
    def find_event(event, year):
        """ Receives a list containing all the information to input to the event """
        sql = 'SELECT * FROM events WHERE event=%s AND year=%s'
        conn = None
        entry = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (event, year))
            entry = cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
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
        # need to search for rider_id and then pass it
        conn = None
        try:
            rider_id = self.find_rider(name, number, bike, year)  # returns a tuple of the entry
            if rider_id is None:
                raise Exception(
                    'Event: ' + event + ' Name: ' + name + ' ' + number + ' bike: ' + bike + ' ' + year + ' Does Not Exist in riders table')
            rider_id = list(rider_id)[0]
            # converts tuple to list because sometimes the accessing tuple return a Nonetype error even though it is type STR

            event_id = self.find_event(event, year)
            if event_id is None:
                raise TypeError('Event does not exist in events table')
            event_id = event_id[0]

            entry = self.find_finish(rider_id, event_id)
            if entry is None:
                sql = 'INSERT INTO finishes (rider_id, event_id, result) VALUES(%s, %s, %s)'
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(sql, (rider_id, event_id, result))
                conn.commit()
                cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def find_finish(rider_id, event_id):
        """ Receives a list with rider name, year, number# (week number of race) """

        # need to use event_id

        sql = 'SELECT * FROM finishes WHERE rider_id=%s AND event_id=%s'
        conn = None
        entry = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (rider_id, event_id))
            entry = cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        finally:
            if conn is not None:
                conn.close()
            return entry

    #################
    # don't really need this function anymore
    #################
    @staticmethod
    def update_finish(rider, year, race_num, finish):

        # Need to verify rider season has already been entered or just have
        race = 'race' + race_num
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
