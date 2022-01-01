from flask import Flask
from flask_cors import CORS
from .views import auth
from db_connect import db

#pip install  Flask_Migrate 해야함
# 해도 안되면 pip install SQLAlchemy==1.3.23
 
#database 설정 

app = Flask(__name__)
app.register_blueprint(auth.bp)

@app.route('/')
def hi():
    return 'hi'


if __name__ == "__main__":
    app.run(debug = True)


