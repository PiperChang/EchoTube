from flask import Flask, Blueprint, request, jsonify
from flask_restx import Resource, Api, Namespace, fields
from .models import users
from db_connect import db
import jwt
import bcrypt
from server.models.users import User


bcrypt = Bcrypt(app)

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route('/register')
class AuthRegister(Resource) :
    def post(self) :
        user_id = request.form['userID']
        password = request.form['password']
        user_name = request.form['user_name']
        # db에 존재하는지 확인하는 쿼리
        if User.query.filter(User.user_id == user_id).first() :
            return {'message' : "Exist ID"},404
        else :
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())  # 비밀번호 
            new_user = User( user_id, password, user_name)
            db.session.add(new_user)
            db.session.commit()
            # pw도 jwt에 포함필요?
            return {
                'Authorization': jwt.encode({'user_id': user_id }, "secret", algorithm="HS256")  # str으로 반환하여 return
            }, 200

@bp.route('/login')
class AuthLogin(Resource) :
    def post(self):
        user_id = request.form['userID']
        password = request.form['password']
        user = User.query.filter(User.user_id == user_id).first()

        if not user :
            return {
                "message": "User Not Found"
            }, 404
        elif not bcrypt.checkpw(password.encode('utf-8') ,user.password) :
            return {
                "message": "Wrong Password"
            }, 500
        else :
            return {
                'Authorization': jwt.encode({'name': name}, "secret", algorithm="HS256") # str으로 반환하여 return
            }, 200