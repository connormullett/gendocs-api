
from flask import request, json, Blueprint, g
from ..models.comment import CommentModel, CommentSchema
from .user_view import custom_response

from ..shared.authentication import Auth


comment_api = Blueprint('comment_api', __name__)
comment_schema = CommentSchema()

@comment_api.route('/', methods=['POST'])
def create_comment():
    '''
    creates a comment associated
    with the owner's id, also
    requires the doc's id
    '''
    req_data = request.get_json()
    req_data['owner_id'] = g.user['id']

    if not req_data.get('doc_id'):
        return custom_response('missing doc id', 400)

    data, error = comment_schema.load(req_data)

    if error:
        return custom_response(error, 404)

    comment = CommentModel(data)
    comment.save()

    com_data = doc_schema.dump(doc).data
    return custom_response(com_data, 201)


@comment_api.route('/<int:doc_id>', methods=['GET'])
def get_all_comments_by_doc_id(doc_id):
    comments = CommentModel.get_replies_from_comment_id(doc_id)
    data = doc_schema.dump(docs, many=True).data
    return custom_response(data, 200)

