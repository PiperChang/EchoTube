from ..db_connect import db

class User(db.Model):
  __tablename__ =  'users'
  id = db.Column(db.Integer, primary_key = True, nullable = False)
  name = db.Column(db.String(20), nullable = False)
  email = db.Column(db.String(255), nullable = False)
  pw = db.Column(db.String(255)  , nullable = False)
  
  #필요 시 외부 키 추가
  def __init__(self,email,pw,name) -> None:
      self.pw = pw
      self.name = name
      self.email = email
