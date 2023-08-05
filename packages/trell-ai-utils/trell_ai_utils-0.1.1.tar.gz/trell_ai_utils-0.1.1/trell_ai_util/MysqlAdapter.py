import os
from subprocess import Popen
import mysql.connector
import pandas as pd
import psutil
from flask import current_app
from sqlalchemy import create_engine

import boto3
import json

try:
    secret_name = "data-secret"
    region_name = "ap-south-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    response = client.get_secret_value(
        SecretId=secret_name
    )
    cred = json.loads(response['SecretString'])
except:
    print("you are not authorized to use Trell pip package")



def insert_row_into_production_table(data, table_name):
    conn = create_engine(cred['DATA_PROD_DB_CONNECTION_STRING'])
    try:
        data.to_sql(name=table_name, con=conn, if_exists='append', index=False)
    finally:
        conn.dispose()

def insert_row_into_production_table_test(data, table_name):
    conn = create_engine(cred['TEST_DB_CONNECTION_STRING'])
    try:
        data.to_sql(name=table_name, con=conn, if_exists='append', index=False)
    finally:
        conn.dispose()

def update_production_data_table_row(query):
    conn = create_engine(cred['DATA_PROD_DB_CONNECTION_STRING'])
    try:
        conn.execute(query)
    finally:
        conn.dispose()

def create_table_in_prod_mysql(query):
    conn = create_engine(cred['DATA_PROD_DB_CONNECTION_STRING'])
    try:
        conn.execute(query)
    finally:
        conn.dispose()

def update_production_data_table_row_test(query):
    conn = create_engine(cred['TEST_DB_CONNECTION_STRING'])
    try:
        conn.execute(query)
    finally:
        conn.dispose()

def get_production_data_from_local(query, write_to_csv=False, filename="trail_loves.csv"):
    cnx = mysql.connector.connect(user=cred['DATA_USER'],
                                  password=cred['DATA_PWD'],
                                  host="127.0.0.1",
                                  port=cred['PORT_1'],
                                  database="trellDb")
    try:
        df = pd.read_sql(query + " ;", cnx)
        if write_to_csv:
            df.to_csv(filename)
        return df
    finally:
        cnx.close()


def get_production_data_from_test(query):
    cnx = mysql.connector.connect(user=cred['TEST_USER'],
                                  password=cred['TEST_PWD'],
                                  host=cred['TEST_HOST'],
                                  port=cred['PORT_2'],
                                  database="trellDb")
    try:
        return pd.read_sql(query + " ;", cnx)
    finally:
        cnx.close()

def get_production_data_from_prod(query):
    cnx = mysql.connector.connect(user=cred['DATA_USER'],
                                  password=cred['DATA_PWD'],
                                  host= cred['PROD_HOST'],
                                  port=cred['PORT_2'],
                                  database="trellDb")
    try:
        return pd.read_sql(query + " ;", cnx)
    finally:
        cnx.close()

def get_analytics_data(query):
    cnx = mysql.connector.connect(user=cred['DATA_USER'],
                                  password=cred['DATA_PWD'],
                                  host=cred['ANAL_HOST'],
                                  port=cred['PORT_2'],
                                  database="trellDb")
    try:
        return pd.read_sql(query + " ;", cnx)
    finally:
        cnx.close()

def write_into_analytics_table(data, table_name, db_name):
    conn = create_engine(cred['DATA_ANAL_DB_STRING'])
    try:
        print("Before to_sql")
        data.to_sql(name=table_name, schema=db_name, con=conn, if_exists='append', index=False)
        # conn.commit()
        print("After to_sql")
    except Exception as e:
        print(e)
    finally:
        conn.dispose()

def get_analytics_events_data(limit=1000, write_to_local = False, debug=False):
    db_connection = create_engine(cred['DATA_ANAL_DB_STRING'])
    df = pd.read_sql('SELECT * FROM events LIMIT ' + str(limit), con=db_connection)
    if debug:
        print(df.head())
    if write_to_local:
        df.to_csv('events.csv')
    return df


def get_production_data(table_name="content", limit=300, write_to_local=False, debug=False):
    cnx = mysql.connector.connect(user=cred['DATA_USER'],
                                  password=cred['DATA_PWD'],
                                  host=cred['PROD_HOST'],
                                  database="trellDb")
    try:
        return pd.read_sql("SELECT * FROM " + str(table_name) + " LIMIT " + str(limit) + " ;", cnx)
    finally:
        cnx.close()


def get_production_data_query(query, write_to_local=False, debug=False):
    cnx = mysql.connector.connect(user=cred['DATA_USER'],
                                  password=cred['DATA_PWD'],
                                  host=cred['PROD_HOST'],
                                  database="trellDb")
    try:
        return pd.read_sql(query + " ;", cnx)
    finally:
        cnx.close()

def delete_from_production_data_query(query):
    cnx = mysql.connector.connect(user=cred['DATA_USER'],
                                  password=cred['DATA_PWD'],
                                  host=cred['PROD_HOST'],
                                  database="trellDb")
    mycursor = cnx.cursor(buffered=True)
    mycursor.execute(query)
    cnx.commit()
    print(mycursor.rowcount, "record(s) deleted")
    mycursor.close()
    cnx.close()

def delete_from_datascience_data_query(query):
    cnx = mysql.connector.connect(user=cred['DATA_USER'],
                                  password=cred['DATA_PWD'],
                                  host=cred['PROD_HOST'],
                                  database="data_science")
    mycursor = cnx.cursor(buffered=True)
    mycursor.execute(query)
    cnx.commit()
    print(mycursor.rowcount, "record(s) deleted")
    mycursor.close()
    cnx.close()

def write_to_table(data, table_name):
    """
    Writes the daily users onto the DB
    """
    current_app.logger.info("Writing {} rows onto the Table \
        dailyUsers".format(data.shape[0]))
    current_app.logger.info(data.dtypes)
    engine = create_engine(cred['DB_CONNECTION_STRING_INTERN'], echo=False)
    data.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    current_app.logger.info("Data Successfully Written into {}".format(table_name))

def connect_to_database():
    current_app.logger.info('Connecting to Database')
    # Check if connection exists
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    if len(children) == 0:
        process = Popen(['./tunnel.sh'])
        return process
    else:
        for child in children:
            p = psutil.Process(child.pid)
            p.terminate()

def check_process():
    """
    Check if /users, /trails have finished
    processing.
    """
    pass


