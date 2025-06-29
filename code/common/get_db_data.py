import sqlite3
import pdb  
#import common.app_globals as app_glob

qry_genre_dist = """
    SELECT Genre,count(*) AS Counts FROM movies
    GROUP BY genre
    ORDER BY GENRE	
    """

def get_table_data(mySQLcursor, table_name):
    query = f"SELECT * FROM {table_name}"
    mySQLcursor.execute(query)
    db_data = mySQLcursor.fetchall()
    return db_data

def get_query_data(mySQLcursor, query):
    mySQLcursor.execute(query)
    db_data = mySQLcursor.fetchall()
    return db_data