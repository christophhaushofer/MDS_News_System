import os
from dotenv import load_dotenv

load_dotenv()

FEED_EXPORT_ENCODING = 'utf-8'
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': os.environ.get("user"),
    'password': os.environ.get("password"),
    'database': os.environ.get("database")
}

