import os
import pandas as pd
from dotenv import load_dotenv
from os.path import join, dirname
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from utility.clean import *
from datetime import datetime as dt
import datetime

def get_data(tablename):

    load_dotenv()
    DATABASE = {
        'drivername': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'username': os.environ.get("user"),
        'password': os.environ.get("password"),
        'database': os.environ.get("database")
    }

    # connect to db an load data
    db_url = URL(**DATABASE)
    engine = create_engine(db_url, client_encoding='utf8')

    data = pd.read_sql_query(f'select * from "{tablename}"', con=engine)
    # fill empty cells with NaN
    data.content = data.content.fillna('').astype(str)

    # calculate number of words for every article
    data['wordCount'] = data.content.apply(lambda x: len(str(x).split(' ')))
    output = pd.DataFrame(data)
    output.id = output.index

    print(f'Found {output.shape[0]} Articles!')
    return (output)


def get_clusters():
    load_dotenv()
    DATABASE = {
        'drivername': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'username': os.environ.get("user"),
        'password': os.environ.get("password"),
        'database': os.environ.get("database")
    }

    # connect to db an load data
    db_url = URL(**DATABASE)
    engine = create_engine(db_url, client_encoding='utf8')

    data = pd.read_sql_query(f'select * from clustered_data', con=engine)
    output = pd.DataFrame(data)
    # output.id = output.index

    print(f'Found {output.shape[0]} Clusters!')
    return (output)

def write_to_db(data, tablename):

    load_dotenv()
    DATABASE = {
        'drivername': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'username': os.environ.get("user"),
        'password': os.environ.get("password"),
        'database': os.environ.get("database")
    }

    # connect to db an load data
    db_url = URL(**DATABASE)
    engine = create_engine(db_url, client_encoding='utf8')

    data.to_sql(tablename, engine, if_exists='replace', index_label="id")





