import jwt
import bcrypt
from flask_restx import Resource, Api, Namespace
from flask_bcrypt import Bcrypt

from flask import request

from ..db_connect import db
from ..models.user import User

Auth = Namespace(
    name="Auth",
    description = "사용자 인증을 위한 API"
)

# 회원가입 
@Auth.route('/register')
class AuthRegister(Resource) :
    # request 객체에 모든 값이 안들어왔을 경우, Key Error 발생 : Front 측에서 Validation ?
    def post(self) :
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        # request 양식 확인
        if None in [email,password,name] :
            return {'message' : "Key error, Please fill in all question"},404
        # 기존 계정 확인
        if User.query.filter(User.email == email).first() :
            return {'message' : "이미 가입된 이메일입니다."}, 404
        else :
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())  # 비밀번호 
            new_user = User(email , password, name)
            db.session.add(new_user)
            db.session.commit()
            
            return {
                'token': jwt.encode({'email': email }, "secret", algorithm="HS256")  # str으로 반환하여 return
            }, 200

# 로그인
@Auth.route('/login')
class AuthLogin(Resource) :
    def post(self):
        email = request.form['email']
        password = request.form['password']
        
        #request 양식 확인
        if None in [email, password] :
            return {'message' : "가입을 위한 양식을 채워주세요.(프론트에서 구현)"}, 404 

        user = User.query.filter(User.email == email).first()
        if user is None :
            return {
                "message": "존재하지 않는 계정입니다."
            }, 404

        elif not bcrypt.checkpw(password.encode("utf-8") ,user.password.encode('utf-8')) :
            return {
                "message": "Wrong Password"
            }, 500
        else :
            return {
                'token': jwt.encode({'email': email }, "secret", algorithm="HS256") # str으로 반환하여 return
            }, 200