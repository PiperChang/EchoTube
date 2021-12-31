from flask import Flask, jsonify, request
from flask_cors import CORS
# from db_connect import db
import config

app = Flask(__name__)

CORS(app)

# session 사용을 위한 secret_key
app.secret_key = config.SECRET_KEY

# SQLAlchemy 객체를 app과 연결
db.init_app(app)
Migrate().init_app(app, db)

# view Blueprint 등록
app.register_blueprint(auth.bp)
app.register_blueprint(oauth.bp)
app.register_blueprint(main.bp)

# 없애기 or 변경..?
@app.route('/')
def get_current_time():
    return 'hello, world!'

if __name__ == "__main__":
    app.run(debug=True)

