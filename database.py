
import psycopg2

from config import config

_conn = None:

def connect():
	"""Connects to the database from the database.ini file."""
	try:
		params = config()
		print('Connecting to the PosgreSQL database...')
		
		_conn = psycopg2.connect(**params)

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def get_cursor():
	"""returns the cursor for the database connection in order to make unique SQL queries."""
	return _conn.cursor()


def disconnect():
	"""Disconnects the database from the database.ini file."""
	try:
		if _conn is not None:
			_conn.close()
			print('Database connection closed.')

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)


# this is probably not needed as an external function.  This should be done automatically
# should probably include this into the connect function.  
# Connect should be able to verify if the tables have been created and if not then create them.
def add_table(name, properties):
	"""Adds a new table to the database: 
	Parameters
	name: the name of the table; 
	properties: a tuple of the attributes for the table."""
	try:
		cur = _conn.cursor()
		# possible method for creating table using a tuple
		# c.execute('''CREATE TABLE table_name {}'''.format(tuple(column_list)))
		cur.execute('CREATE TABLE ')



def add_record(record, table):
	"""Inserts a new record into thenamed table.
	Parameters
	record: list of the attributes to be inserted
	table: the name of the table to insert record to."""

# do I need a search?
# I need to pass the cursor so that I can be specific SQL calls to the 
	







