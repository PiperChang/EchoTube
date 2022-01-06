from flask import Flask, request, jsonify, render_template
from models import Video_Tag, Tag, Video
from db_connect import db
from sqlalchemy import and_
import json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


with open('config.json', 'r') as f:
    config = json.load(f)

user = config['database']['user']
password = config['database']['password']
host = config['database']['host']
port = config['database']['port']
dbname = config['database']['dbname']

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

result = []


@app.route("/")
def home():
    return ''


@app.route("/search-tag", methods=['GET'])
def search_tag():

    result.clear()  # 검색 할때마다 result를 초기화
    tag = request.args['tag']
    category = request.args['category']
    page = request.args.get('page', type=int, default=1)  # 페이지
    per_page = 9 # 페이지 당 보여질 video 수
    video = None  # 출력할 1개의 비디오 영상
    video_list = []

    # 입력 받은 tag를 검색
    tag_obj = Tag.query.filter(Tag.name == tag).first()

    # 입력 받은 tag의 tag_id를 가지고 있는 Video_Tag 객체들을 리스트로 반환
    video_tag_objs = Video_Tag.query.filter(
                     Video_Tag.tag_id == tag_obj.id).all()

    for video_tag_obj in video_tag_objs:
        if category:
            # video_tag_obj의 id와 category에 해당하는 유일한 Video 객체를 반환
            video = Video.query.filter(and_(
                    Video.id == video_tag_obj.video_id,
                    Video.category_id == category)).first()
            video_list.append(video)
        else:
            # 카테고리를 선택 안 한 경우 video_tag_obj의 id에 해당하는 유일한 Video 객체를 반환
            video = Video.query.filter(
                    Video.id == video_tag_obj.video_id).first()
            video_list.append(video)

        if video is None:
            continue

    if len(video_list) <= per_page * page - per_page:
        result = 0
    else:
        
        video_list = video_list.paginate(page, per_page=9)  

        '''# 프론트엔드에 전달할 데이터
        result.append(
            {'index': video.id,
             'title': video.title,
             'video_id': video.video_code,
             'published_date': video.published_at,
             'tags': video.tags,
             'catagory_id': video.category_id
             }
        )'''

    

    return jsonify(video_list)

@app.route("/list")
def list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Video.query.order_by(Video.id)
    print(type(question_list))
    question_list = question_list.paginate(page, per_page=10)
    return render_template('index.html', rows=question_list)


if __name__ == '__main__':
    app.run()
