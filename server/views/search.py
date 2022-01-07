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
    "{'tags':'행복, 감사','categoryId':24,'page':1}"
    )
})

category_fields = Search.model('Tag', {
    'data' : fields.String(description='data', required=True, example=
    "{'categoryId':24,'page':1}"
    )
})


@Search.route('/tags')
class Search_tag(Resource) :
  @Search.expect(category_tag_fields)
  @Search.doc(responses={200:'Success'})

  def get(self) :
    """여러 개의 tag들에 해당하는 영상을 반환합니다."""
    video_result = []
    vedio_list = []

    data = request.args["data"]  # 요청 데이터

    try:
        data = eval(data)  # data를 문자열에서 dict로 변환
    except:
        return jsonify('태그와 카테고리를 모두 입력하세요.')

    tag_list = data['tags']
    tag_list = tag_list.split(',')
    tag_list = [tag.strip() for tag in tag_list]

    category_id = int(data['categoryId'])
    page = int(data['page'])

    if page == 0 : return jsonify('페이지 값은 1이상이어야 합니다.')

    per_page = 9
    
    for i in range(len(tag_list)):
        # 입력 받은 tag를 검색
        tag = Tag.query.filter(Tag.name == tag_list[i]).first()

        if tag is None:
            continue

        # 입력 받은 tag의 tag_id를 가지고 있는 VideoTag 객체들을 리스트로 반환
        video_tags = VideoTag.query.filter(
                        VideoTag.tag_id == tag.id).all()

        for video_tag in video_tags:
            video = Video.query.filter(Video.id == video_tag.video_id)
            video = video.first() if category_id == 0 else video.filter(Video.category_number==category_id).first()
            
            if video is None:
                continue
     
            vedio_list.append({
                'title': video.title,
                'channel' : video.channel,
                'thumbnail' : video.thumbnail,
                'videoAddress': video.video_address,
                'categoryId': video.category_number,
                'likes' : video.likes,
                'views' : video.views
                }
            )


    max_page = math.ceil(len(vedio_list) / per_page)

    if len(vedio_list) == 0:
        max_page =  1
    
    if page > max_page:
        return jsonify('다음 페이지가 존재하지 않습니다.')

    start_index = per_page * (page-1)
    end_index = (page * per_page) - 1
        
    if page == max_page:
            end_index = len(vedio_list) - 1
        
    for i in range(start_index, end_index+1):
        
        video_result.append({
            'title': vedio_list[i]['title'],
            'channel' : vedio_list[i]['channel'],
            'thumbnail' : vedio_list[i]['thumbnail'],
            'videoAddress': vedio_list[i]['videoAddress'],
            'categoryId': vedio_list[i]['categoryId'],
            'likes' : vedio_list[i]['likes'],
            'views' : vedio_list[i]['views']
        }) 

    if len(video_result) != 0:
        video_result = sorted(video_result, key=lambda x:x['views'], reverse=True)

    result = {}
    result['videos'] = video_result
    result['max_page'] = max_page

    return jsonify(result)

@Search.route('/category')
class Search_tag(Resource) :
  @Search.expect(category_fields)
  @Search.doc(responses={200:'Success'})

  def get(self) :
    """카테고리에 해당하는 영상을 9개 반환합니다."""
    video_result = []
    data = request.args["data"]  # 요청 데이터

    try:
        data = eval(data)  # data를 문자열에서 dict로 변환
    except:
        return jsonify('카테고리와 페이지를 모두 입력하세요.')
        
    category_id = int(data['categoryId'])
    page = int(data['page'])
    if page == 0 : return jsonify('페이지 값은 1이상이어야 합니다.')

    # 전체 카테고리일 떄
    if category_id == 0:
        video = Video.query.all()
    else:
    # 입력 받은 category_id를 가지고 있는 Video 객체들을 리스트로 반환
        video = Video.query.filter(Video.category_number == category_id).all()

    per_page = 9
    max_page = math.ceil(len(video) / per_page)

    if len(video) == 0:
        max_page = 1

    if page > max_page:
        return jsonify('다음 페이지가 존재하지 않습니다.')

    start_index = per_page * (page-1)
    end_index = (page * per_page) - 1
        
    if page == max_page:
            end_index = len(video) - 1
        
    for i in range(start_index, end_index+1):
        
        video_result.append({
            'title': video[i].title,
            'channel' : video[i].channel,
            'thumbnail' : video[i].thumbnail,
            'videoAddress': video[i].video_address,
            'categoryId': video[i].category_number,
            'likes' : video[i].likes,
            'views' : video[i].views
        })

    if len(video_result) != 0:
        video_result = sorted(video_result, key=lambda x:x['views'], reverse=True)

    result = {}
    result['videos'] = video_result
    result['max_page'] = max_page

    return jsonify(result)