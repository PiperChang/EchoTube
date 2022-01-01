from flask import Flask, request, jsonify, render_template
from models import Post, Post_Tag, Tag
from db_connect import db


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

    #입력 받은 tag를 검색
    tag_obj = Tag.query.filter(Tag.tag_name == tag).first()
    
    #입력 받은 tag의 tag_id를 가지고 있는 Post_Tag 객체들을 리스트로 반환
    post_tag_objs = Post_Tag.query.filter(Post_Tag.tag_id == tag_obj.tag_id).all()
    
    for post_tag_obj in post_tag_objs:

        #post_tag_obj의 post_index에 해당하는 유일한 Post 객체를 반환
        post_info = Post.query.filter(post_tag_obj.post_index == Post.post_index ).first()

        #프론트엔드에 전달할 데이터
        result.append(
            {'post_index':post_info.post_index,
             'title':post_info.title,
             'video_id':post_info.video_id,
             'published_date':post_info.published_date,
             'tags':post_info.tags,
             'catagory_id':post_info.category_id
            }
        )

    return jsonify(result)

'''@app.route("/search-category", methods = ['POST'])
def search_category():
    data = request.get_json()
    category = data['category']'''

if __name__ == '__main__':
    app.run()