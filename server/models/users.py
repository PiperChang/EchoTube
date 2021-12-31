from db_connect import db

class User(db.model):
  __tablename__ =  'user_tb'
  user_id = db.Column(db.Integer, primary_key = True, nullable = False)
  user_pw = db.Column(db.String(255)  , nullable = False)
  user_name = db.Column(db.String(20), nullable = False)

  #필요 시 외부 키 추가
  def __init__(self,id,pw,name,age) -> None:
      self.user_id = id
      self.user_pw = pw
      self.user_name = name

