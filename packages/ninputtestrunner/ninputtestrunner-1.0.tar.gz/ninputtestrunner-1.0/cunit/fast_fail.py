
"""

The idea of the method is to stop the analysis once VyPR detects a verdict failure.
We look at the database for getting verdict information

"""

import sqlite3
from os.path import dirname, abspath

ROOT_DIR = dirname(dirname(abspath(__file__)))

def fail_fast_check():
	try:
		sqliteConnection = sqlite3.connect(ROOT_DIR+'/VyPRServer/verdicts.db')

		cursor = sqliteConnection.cursor()

		sqlite_query = "select COUNT(*)  from verdict where verdict = 0;"
		cursor.execute(sqlite_query)


		record = cursor.fetchall()

		cursor.close()

	except sqlite3.Error as error:

		print("Error while connecting to sqlite", error)

	finally:

		if (sqliteConnection):

			sqliteConnection.close()

	return record[0][0]

