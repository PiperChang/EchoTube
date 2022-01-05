from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields

from ..db_connect import db
from ..models.models import Tag, Video, Video_Tag
from sqlalchemy import and_
import json
import math

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


# http://127.0.0.1:5000/search/search-tag?tag=행복&tag=감사&category=24
# http://127.0.0.1:5000/search/search-tag?tag=행복&tag=감사&category=24
''' http://127.0.0.1:5000/search/search-tag?data={
    "tags":['행복', '감사'],
    "categoryId":24}
'''

''' http://127.0.0.1:5000/search/search-tag?data={
    "tags":['행복', '감사'],
    "categoryId":0}
'''

''' http://127.0.0.1:5000/search/category?data={
    "categoryId":24,
    "page":1
    }
'''

@Search.route('/search-tag')
class Search_tag(Resource) :
  @Search.expect(category_tag_fields)
  @Search.doc(responses={200:'Success'})

  def get(self) :

    result = []

    data = request.args["data"]  # 요청 데이터

    data = eval(data) # tag를 문자열에서 dict로 변환
    
    '''print("type: ", type(data))
    print(data['tags'])
    print(type(data['tags']))  #list
    print(data['tags'][0])'''

    tag_list = data['tags']
    category_id = int(data['categoryId'])


    for i in range(len(tag_list)):
        #print("1. ",tag_list[i])
        # 입력 받은 tag를 검색
        tag_obj = Tag.query.filter(Tag.name == tag_list[i]).first()
        #print("2. ",tag_obj)

        # 입력 받은 tag의 tag_id를 가지고 있는 Video_Tag 객체들을 리스트로 반환
        video_tag_objs = Video_Tag.query.filter(
                        Video_Tag.tag_id == tag_obj.id).all()

        for video_tag_obj in video_tag_objs:
            if category_id:
                # video_tag_obj의 id와 category에 해당하는 유일한 Video 객체를 반환
                video = Video.query.filter(and_(
                        Video.id == video_tag_obj.video_id,
                        Video.category_number == category_id)).first()
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
  @Search.expect(category_tag_fields)
  @Search.doc(responses={200:'Success'})

  def get(self) :

    result = []

    data = request.args["data"]  # 요청 데이터

    data = eval(data) # tag를 문자열에서 dict로 변환
        
    '''print("type: ", type(data))
    print(data['tags'])
    print(type(data['tags']))  #list
    print(data['tags'][0])'''
    category_id = int(data['categoryId'])
    page = int(data['page'])
    print("page는 ",page) 

    # 입력 받은 category_id를 가지고 있는 Video 객체들을 리스트로 반환
    video = Video.query.filter(Video.category_number == category_id).all()

    
    per_page = 9
    max_page = math.ceil(len(video) / per_page)

    if page > max_page:
        return jsonify('다음 페이지가 존재하지 않습니다.')
    start_index = per_page * (page-1)
    end_index = (page * per_page) - 1

    print("start_index는 ",start_index)   
    print("max_page는 ",max_page)
    print("end_index ",end_index)  

    
        
    if page == max_page:
            end_index = len(video) - 1
        
    print('시작')
    print("start_index는 ", start_index)
    print("end_index는 ", end_index)
    for i in range(start_index, end_index+1):
        print("i는 ", i)

        result.append({
            'title': video[i].title,
            'channel' : video[i].channel,
            'thumbnail' : video[i].thumbnail,
            'videoAddress': video[i].video_address,
            'categoryId': video[i].category_number,
            'likes' : video[i].likes,
            'views' : video[i].views
        })

    print("aa의 길이는 ",len(result))
    result = sorted(result, key=lambda x:x['views'], reverse=True)
    return jsonify(result)


