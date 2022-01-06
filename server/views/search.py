from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields

from ..db_connect import db
from ..models.models import Tag, Video, VideoTag
from sqlalchemy import and_
import json
import math

Search = Namespace(
  name="Search",
  description = "Tag를 통한 트렌드 동영상 검색 API"
)


category_tag_fields = Search.model('Tag and Category', {
    'data' : fields.String(description='data', required=True, example=
    "{'tags':['행복','감사'],'categoryId':24}"
    )
})

category_fields = Search.model('Tag', {
    'data' : fields.String(description='data', required=True, example=
    "{'categoryId':24,'page':1}"
    )
})

# 예시
''' http://127.0.0.1:5000/search/tags?data={
    "tags":['행복', '감사'],
    "categoryId":24}
'''

''' http://127.0.0.1:5000/search/tags?data={
    "tags":['행복', '감사'],
    "categoryId":0}
'''

''' http://127.0.0.1:5000/search/category?data={
    "categoryId":24,
    "page":1}
'''

@Search.route('/tags')
class Search_tag(Resource) :
  @Search.expect(category_tag_fields)
  @Search.doc(responses={200:'Success'})

  def get(self) :
    """여러 개의 tag들에 해당하는 영상을 반환합니다."""
    result = []

    data = request.args["data"]  # 요청 데이터

    #data = eval(data) # data를 문자열에서 dict로 변환

    try:
        data = eval(data)
    except:
        return jsonify('태그와 카테고리를 모두 입력하세요.')

    tag_list = data['tags']
    category_id = int(data['categoryId'])


    for i in range(len(tag_list)):
        # 입력 받은 tag를 검색
        tag = Tag.query.filter(Tag.name == tag_list[i]).first()

        # 입력 받은 tag의 tag_id를 가지고 있는 VideoTag 객체들을 리스트로 반환
        video_tags = VideoTag.query.filter(
                        VideoTag.tag_id == tag.id).all()

        for video_tag in video_tags:
            video = Video.query.filter(Video.id == video_tag.video_id)
            video = video.first() if category_id is 0 else video.filter(Video.category_number==category_id).first()
            
            if video is None:
                continue
                
            result.append({
                'title': video.title,
                'channel' : video.channel,
                'thumbnail' : video.thumbnail,
                'videoAddress': video.video_address,
                'categoryId': video.category_number,
                'likes' : video.likes,
                'views' : video.views
                }
            )
    result = sorted(result, key=lambda x:x['views'], reverse=True)
    return jsonify(result)

@Search.route('/category')
class Search_tag(Resource) :
  @Search.expect(category_fields)
  @Search.doc(responses={200:'Success'})

  def get(self) :
    """카테고리에 해당하는 영상을 9개 반환합니다."""
    result = []

    data = request.args["data"]  # 요청 데이터

    try:
        data = eval(data)  # data를 문자열에서 dict로 변환
    except:
        return jsonify('카테고리와 페이지를 모두 입력하세요.')
        
    category_id = int(data['categoryId'])
    page = int(data['page'])
    if page == 0 : return jsonify('페이지 값은 1이상이어야 합니다.')

    # 입력 받은 category_id를 가지고 있는 Video 객체들을 리스트로 반환
    video = Video.query.filter(Video.category_number == category_id).all()

    per_page = 9
    max_page = math.ceil(len(video) / per_page)

    if page > max_page:
        return jsonify('다음 페이지가 존재하지 않습니다.')

    start_index = per_page * (page-1)
    end_index = (page * per_page) - 1
        
    if page == max_page:
            end_index = len(video) - 1
        
    for i in range(start_index, end_index+1):
  
        result.append({
            'title': video[i].title,
            'channel' : video[i].channel,
            'thumbnail' : video[i].thumbnail,
            'videoAddress': video[i].video_address,
            'categoryId': video[i].category_number,
            'likes' : video[i].likes,
            'views' : video[i].views
        })

    result = sorted(result, key=lambda x:x['views'], reverse=True)
    return jsonify(result)


