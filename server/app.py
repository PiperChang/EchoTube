from flask import Flask, request, render_template, jsonify
import jwt

app = Flask(__name__)
encryption_secret = "east"
algorithm = "HS256"
origin = {"name":"name", "password":"r432"}



@app.route("/", methods=["POST"]) 
def jwt_route(): 
    id = request.form['username']
    pw = request.form['password']
    if origin['name'] == id and origin['password'] == pw :
        data_to_encode = {'name':id,'password':pw }
        encoded = jwt.encode(data_to_encode, encryption_secret, algorithm = algorithm).decode()
        decoded = jwt.decode(encoded, encryption_secret, algorithm = [algorithm])
        data = {"encoded" : encoded, "decoded" : decoded}
        return data
    else :
        return "Wrong"


if __name__ == "__main__":
    app.run(debug = True)