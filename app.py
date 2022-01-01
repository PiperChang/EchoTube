from flask import Flask, request, jsonify, render_template
from models import Video_Tag, Tag, Video
from db_connect import db
from sqlalchemy import and_


app = Flask(__name__)

#database 설정파일
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:0000@localhost:\
    3306/mydb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

result = []

@app.route("/")
def home():
    return render_template('index.html', rows = result)


@app.route("/search-tag", methods = ['POST'])
def search_tag():

    result.clear() #검색 할때마다 result를 초기화

    data = request.get_json()

    tag = data['tag']

    category = 0
    if data['category'] != '':
        category = int(data['category'])
    

    #입력 받은 tag를 검색
    tag_obj = Tag.query.filter(Tag.name == tag).first()
    
    #입력 받은 tag의 tag_id를 가지고 있는 Video_Tag 객체들을 리스트로 반환
    video_tag_objs = Video_Tag.query.filter(Video_Tag.tag_id == tag_obj.id).all()
    
    for video_tag_obj in video_tag_objs:
        video_info = None
        if category:
            #video_tag_obj의 id에 해당하는 유일한 Video 객체를 반환
            video_info = Video.query.filter(and_(Video.id == video_tag_obj.video_id, \
                        Video.category_id == category)).first()
        else:
            video_info = Video.query.filter(Video.id == video_tag_obj.video_id).first()
        
        if video_info is None:
            continue

        #프론트엔드에 전달할 데이터
        result.append(
            {'index':video_info.id,
             'title':video_info.title,
             'video_id':video_info.video_id_name,
             'published_date':video_info.published_at,
             'tags':video_info.tags,
             'catagory_id':video_info.category_id
            }
        )

    return jsonify(result)


if __name__ == '__main__':
    app.run()