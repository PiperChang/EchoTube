from db_connect import db


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    video_code = db.Column(db.String(45), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    published_at = db.Column(db.DateTime, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(1000), nullable=False)

    def __init__(self, video_id, title, published_date, category_id, tags):
        self.video_id = video_id
        self.title = title
        self.published_date = published_date
        self.category_id = category_id
        self.tags = tags


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
