from flask_restx import Resource, Api, Namespace
from flask import request

from ..db_connect import db
from ..models.models import Tag, Video, Video_Tag

Search = Namespace(
  name="Search",
  description = "Tag를 통한 트렌드 동영상 검색 API"
)

@Search.route('/search-tag')
class Search_tag(Resource) :
  def post(self) :
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
