from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Resource, Api
from .db_connect import db

# #local 에서 바로 import로 실행시 에러 발생. 일일이 상대 참조해야 함
from .views.auth import Auth
from . import config


app = Flask(__name__) # app은 플라스크로 만든 객체이다.
api = Api(app)

CORS(app)

# config 파일의 mysql 주소로 연동
app.config.from_object(config)
db.init_app(app)
Migrate().init_app(app,db)

api.add_namespace(Auth,'/auth')

if __name__ == '__main__':
    app.run()