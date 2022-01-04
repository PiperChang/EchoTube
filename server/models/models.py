from ..db_connect import db


class User(db.Model):
  __tablename__ =  'users'
  id = db.Column(db.Integer, primary_key = True, nullable = False)
  name = db.Column(db.String(20), nullable = False)
  email = db.Column(db.String(255), nullable = False)
  password = db.Column(db.String(255)  , nullable = False)
  
  def __init__(self,email,password,name) -> None:
      self.password = password
      self.name = name
      self.email = email


class Video(db.Model):
  __tablename__ = 'videos'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  video_address = db.Column(db.String(200), nullable=False)  
  published_at = db.Column(db.DateTime, nullable=False)
  category_number = db.Column(db.Integer, nullable=False)
  tags = db.Column(db.String(1000), nullable=False)
  likes = db.Column(db.Integer, nullable=False)
  views = db.Column(db.Integer, nullable=False)
  channel = db.Column(db.String(100), nullable=False)
  thumbnail = db.Column(db.String(1000), nullable=False)

  def __init__(self, id, title,video_address, published_at, category_number, tags, views, likes,  channel,thumbnail):
        self.id = id
        self.title = title
        self.video_address = video_address
        self.published_at = published_at
        self.category_number = category_number
        self.tags = tags
        self.likes = likes 
        self.views = views
        self.channel = channel
        self.thumbnail = thumbnail

class Video_Tag(db.Model):
    __tablename__ = 'video_tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer,  db.ForeignKey('videos.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)

    def __init__(self, id, post_id, tag_id):
        self.id = id
        self.post_id = post_id
        self.tag_id = tag_id

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

