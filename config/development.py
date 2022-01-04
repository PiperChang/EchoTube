from config.default import *

import json

with open('config.json', 'r') as f:
    config = json.load(f)

user = config['database']['user']
password = config['database']['password']
host = config['database']['host']
port = config['database']['port']
dbname = config['database']['dbname']

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"