from flask import request, jsonify

from flask_restx import Resource, Api, Namespace, fields

from ..db_connect import db
from ..models.models import Tag, Video, Video_Tag

from ..static.top20_tags import top20_tags

Search = Namespace(
    name="Search",
    description="Tag를 통한 트렌드 동영상 검색 API"
)

category_fields = Search.model('Category', {
    'category': fields.Integer(description='category', required=True, example='24')
})

category_tag_fields = Search.inherit('Tag and Category', category_fields, {
    'tag': fields.String(description='tag', required=True, example='백종원'),
})


@Search.route('/')
class TagsByCategory(Resource):
    @Search.expect(category_fields)
    @Search.doc(responses={200: 'Success'})
    def get(self):
      category = request.args["category"]
      if int(category) not in [0, 1, 2, 10, 15, 17, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29]:
        return {"message": "Wrong category number"}
      return top20_tags[category], 200
