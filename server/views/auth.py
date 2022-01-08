import jwt
import bcrypt

from flask_restx import Resource, Api, Namespace, fields
from flask import request

from db_connect import db
from models.models import User

Auth = Namespace(
    name="Auth",
    description = "사용자 인증을 위한 API"
)


register_fields = Auth.model('Register', {
    'email' : fields.String(description='email', required=True, example='hi@exam.com'),
    'name' : fields.String(description='name', required=True, example='KimChanghui'),
    'password' : fields.String(description='password', required=True, example='password1!')
})

login_fields = Auth.model('Login', {
    'email' : fields.String(description='email', required=True, example='hi@exam.com'),
    'password' : fields.String(description='password', required=True, example='password1!')
})

# 회원가입 
@Auth.route('/register')
class AuthRegister(Resource) :
    @Auth.expect(register_fields)
    @Auth.doc(responses={200:'Success'})
    @Auth.doc(responses={404:"이미 가입된 이메일입니다."})
    def post(self) :
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        # 양식 확인
        if None in [email,password,name] :
            return {'message' : "Key error, Please fill in all question"},404
        # 기존 계정 확인
        if User.query.filter(User.email == email).first() :
            return {'message' : "이미 가입된 이메일입니다."}, 404
        else :
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) 
            new_user = User(email , password, name)
            db.session.add(new_user)
            db.session.commit()
            
            return {
                'token': jwt.encode({'email': email }, "secret", algorithm="HS256")  
            }, 200

# 로그인
@Auth.route('/login')
class AuthLogin(Resource) :
    @Auth.expect(login_fields)
    @Auth.doc(responses={200:'Success'})
    @Auth.doc(responses={404:"존재하지 않는 계정입니다."})
    @Auth.doc(responses={500:"Wrong Password"})
    def post(self):
        email = request.form['email']
        password = request.form['password']
    
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
                'token': jwt.encode({ 'email': email ,"name" : User.name }, "secret", algorithm="HS256"),
            }, 200

@Auth.route('/get')
class AuthGet(Resource) :
    @Auth.doc(responses={200:'Success'})
    @Auth.doc(responses={404:'Login Failed'})
    def get(self) :
        header = request.headers.get('Authorization')
        if header == None:
            return {"message": "Please Login"} , 404
        data = jwt.decode(header,"secret", algorithms="HS256")
        return data, 200

        # secret, algorithm은 보안 문제로 별도의 모듈로 이용하여야 한다.
