from flask import Flask, request, render_template, jsonify
# jwt 모듈을 import하세요.
import jwt

app = Flask(__name__)
encryption_secret = "secret_elice"
algorithm = "HS256"
#인증해줄 사용자 data
origin = {"name":"elice", "password":"elice@1234"}

@app.route("/", methods=["GET","POST"])
def jwt_route():
    # 조건문을 이용해 API 요청을 구분하세요.
    if request.method == 'POST' :
        # POST 방식으로 전송된 username과 password를 변수에 저장하세요.
        id = request.form['username']
        pw = request.form['password']
        # origin에 저장된 name, password와 비교하세요.
        if origin['name'] == id and origin['password'] == pw :
            # 정보가 일치하는 경우 사용자 변수를 만들기 위한 dictionary를 선언하세요.
            data_to_encode = {'name':id,'password':pw }
            # 인증이 완료되면 전송할 encode, decode 정보를 저장하세요.
            encoded = jwt.encode(data_to_encode, encryption_secret, algorithm = algorithm).decode()
            decoded = jwt.decode(encoded, encryption_secret, algorithm = [algorithm])
            # 저장한 정보를 json 형태로 전송하세요.
            data = {"encoded" : encoded, "decoded" : decoded}
            
            return jsonify(data)
        # 정보가 일치하지 않는 경우 "User Not Found"를 화면에 출력하세요.
        else : 
            return jsonify("User Not Found")
    else :
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug = True)