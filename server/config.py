# # SQLAlchemy 세팅
import os

# 현재 폴더 불러오는 것
BASE_DIR = os.path.dirname(__file__)

db = {
    'user'     : 'root',
    'password' : 'qlalfqjsgh123!',
    'host'     : '127.0.0.1',
    'port'     : '3306',
    'database' : 'Sixteen_local'
}
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8" 
SQLALCHEMY_TRACK_MODIFICATIONS = False

