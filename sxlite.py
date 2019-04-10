#sxlite
# is a class that allows access to a specific database for SX Stats

import sqlite3
from sqlite3 import Error

class sxlite:
	# any paramters here (parameters cannot be made private only marked as do not use)

	"""Checks if databse is created if not it creates it"""
	def connect():
		try:
			conn = sqlite3.connect(db_file)

		except Error as e:
			print(e)

		return conn

	def disconnect():
		try:
			conn.close()
		except Error as e:
			print(e)
		return None

	def create_table(sql):
		conn = connect()

		if conn is not None:
			cur = conn.cursor()
			cur.execute(sql)