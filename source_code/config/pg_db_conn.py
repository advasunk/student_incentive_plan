import pandas as pd
import psycopg2 as db_connect

import config.config as config

# from fastapi import Depends

# from config.pg_db_conn_sqlalchemy import db_session
# from config.pg_db_conn_sqlalchemy import engine

# pre-load database connection properties

DATABASE_HOST = config.get_property('PG_DB_HOST')
DATABASE_PORT = config.get_property('PG_DB_PORT')
DATABASE_NAME = config.get_property('PG_DB_NAME')
DATABASE_USERNAME = config.get_property('PG_DB_USER')
DATABASE_PASSWORD = config.get_property('PG_DB_PASSWORD')

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"


def get_db_url():
    return DATABASE_URL


# define function to return a connection to the database
def get_db_connection():
    connection = db_connect.connect(host=DATABASE_HOST, user=DATABASE_USERNAME, password=DATABASE_PASSWORD,
                                    database=DATABASE_NAME)
    # use the below code if you want to use the connection pool from sqlalchemy
    # however, this will not work with save query method as save query method uses psycopg2/curson
    # connection = engine.connect()
    return connection


# define function to return a cursor to the database
def get_db_cursor(connection):
    cursor = connection.cursor()
    return cursor


# define function to close the connection to the database
def close_db_connection(connection):
    connection.close()


# define function to close the cursor to the database
def close_db_cursor(cursor):
    cursor.close()


# define function to execute a query
def execute_query_with_connection(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()
    return cursor.fetchall()


# define function to execute a query
def execute_query_with_cursor(cursor, query):
    cursor.execute(query)
    # return cursor.fetchall()
    # get results as data dictionary
    results = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

    return results


def execute_query(query, ret_data_as_df=True):
    # print('>>>> executing query: ' + query)
    connection = get_db_connection()
    if ret_data_as_df:
        results = pd.read_sql(query, connection)
    else:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
    connection.close()

    if results.empty:
        results = []
    else:
        # replace None with empty string
        results = results.fillna('')

    return results


def save_query(query):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return True


# define function to router_test sample query
def test_sample_query():
    connection = get_db_connection()
    query = "select * from student_incentive_plan.user "
    results = execute_query(query)
    connection.close()
    return results


def execute_insert(sql, params):
    # replace %s with params
    sql = sql.replace('%s', '{}')
    sql = sql.format(*params)
    # print(sql)
    return save_query(sql)


# define main function
if __name__ == "__main__":
    results = test_sample_query()
    print(results)
    print("No of records: " + str(len(results)))
    for each_row in results:
        print(each_row)
