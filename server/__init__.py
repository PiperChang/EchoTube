from flask import Flask
from sqlalchemy import create_engine

from flask_cors import CORS
from . import db_connect

from .views import auth
from . import config
#local 에서 바로 import로 실행시 에러 발생. 일일이 상대 참조해야 함

def create_app():
    app = Flask(__name__) #app은 플라스크로 만든 객체이다.
    
    app.config.from_object(config)
    database = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], encoding = 'utf-8', max_overflow = 0)
    app.database = database    

    app.register_blueprint(auth.bp)

    return app