from db_connect import db


class Post(db.Model):
    __tablename__ = 'post'
    post_index = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(45), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.String(45), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(1000), nullable=False)

    def __init__(self,video_id , title,published_date,category_id,tags):
        self.video_id = video_id
        self.title = title
        self.published_date = published_date
        self.category_id = category_id
        self.tags = tags

class Post_Tag(db.Model):
    __tablename__ = 'post_tag'
    tag_index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_index = db.Column(db.Integer,  db.ForeignKey('post.post_index'),nullable=False)
    tag_id = db.Column(db.Integer, nullable=False)

    def __init__(self,tag_index , post_index,tag_id):
        self.tag_index = tag_index
        self.post_index = post_index
        self.tag_id = tag_id


class Tag(db.Model):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(1000) ,nullable=False)

    def __init__(self,tag_id , tag_name):
        self.tag_id = tag_id
        self.tag_name = tag_name 