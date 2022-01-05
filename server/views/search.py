from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields

from ..db_connect import db
from ..models.models import Tag, Video, Video_Tag

Search = Namespace(
  name="Search",
  description = "Tag를 통한 트렌드 동영상 검색 API"
)

tag_fields = Search.model('Tag', {
    'email' : fields.String(description='email', required=True, example='hi@exam.com'),
    'name' : fields.String(description='name', required=True, example='KimChanghui'),
    'password' : fields.String(description='password', required=True, example='password1!')
})

category_tag_fields = Search.model('Tag and Category', {
    'tag' : fields.String(description='tag', required=True, example='백종원'),
    'category' : fields.Integer(description='category', required=True, example='24')
})


# http://127.0.0.1:5000/search/search-tag?tag=행복&category=24
@Search.route('/search-tag')
class Search_tag(Resource) :
  @Search.expect(category_tag_fields)
  @Search.doc(responses={200:'Success'})

  def get(self) :
    result = []

    tag = request.args["tag"]
    category = request.args["category"]

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
        else:
            # 카테고리를 선택 안 한 경우 video_tag_obj의 id에 해당하는 유일한 Video 객체를 반환
            video = Video.query.filter(
                    Video.id == video_tag_obj.video_id).first()

        if video is None:
            continue
        
        result.append({
            'title': video.title,
            'channel' : video.channel,
            'thumbnail' : video.thumbnail,
            'video_address': video.video_address,
            'category_number': video.category_number,
            'likes' : video.likes,
            'views' : video.views
            }
        )
        return jsonify(result), 200
