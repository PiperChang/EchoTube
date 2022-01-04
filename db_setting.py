# database 설정파일
import json

with open('config.json', 'r') as f:
    config = json.load(f)

user = config['database']['user']
password = config['database']['password']
host = config['database']['host']
port = config['database']['port']
dbname = config['database']['dbname']

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False