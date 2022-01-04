import jwt

from flask import Blueprint, request
from flask_restx import Resource

from flask_bcrypt import Bcrypt

from ..models.users import User

bcrypt = Bcrypt()
bp = Blueprint('auth', __name__, url_prefix="/auth")

# 회원가입 
@bp.route('/register')
class AuthRegister(Resource) :
    # request 객체에 모든 값이 안들어왔을 경우, Key Error 발생 : Front 측에서 Validation ?
    def post(self) :
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        # request 객체에 모든 값이 들어오지 않았을 때
        if None in [email,password,name] :
            return {'message' : "Key error, Please fill in all question"},404
        # db에 존재하는지 확인하는 쿼리
        if User.query.filter(User.email == email).first() :
            return {'message' : "Exist ID"},404
        else :
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())  # 비밀번호 
            new_user = User( email , password, name)
            db.session.add(new_user)
            db.session.commit()
            
            return {
                'token': jwt.encode({'email': email }, "secret", algorithm="HS256")  # str으로 반환하여 return
            }, 200

# 로그인
@bp.route('/login')
class AuthLogin(Resource) :
    def post(self):
        email = request.form['email']
        password = request.form['password']
        if None in [email, password] :
            return {'message' : "Key error, Please fill in all question"},404 
        user = User.query.filter(User.email == email).first()
        
        # Authentification 
        if user is None :
            return {
                "message": "User Not Found"
            }, 404
        elif not bcrypt.checkpw(password.encode('utf-8') ,user.password) :
            return {
                "message": "Wrong Password"
            }, 500
        else :
            return {
                'token': jwt.encode({'email': email }, "secret", algorithm="HS256") # str으로 반환하여 return
            }, 200