
from flask import request, json, Blueprint, g
from ..models.comment import CommentModel, CommentSchema
from .user_view import custom_response

from ..shared.authentication import Auth


comment_api = Blueprint('comment_api', __name__)
comment_schema = CommentSchema()

@comment_api.route('/', methods=['POST'])
@Auth.auth_required
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

    com_data = comment_schema.dump(comment).data
    return custom_response(com_data, 201)


@comment_api.route('/doc/<int:doc_id>', methods=['GET'])
@Auth.auth_required
def get_all_comments_by_doc_id(doc_id):
    comments = CommentModel.get_all_comments_by_doc_id(doc_id)
    data = comment_schema.dump(comments, many=True).data
    return custom_response(data, 200)


@comment_api.route('/<int:comment_id>', methods=['GET', 'DELETE', 'PUT'])
@Auth.auth_required
def comment_actions(comment_id):
    '''
    Allows for update, delete,
    and get methods on a single
    comment, update and delete
    only allowed if user_id from g
    matches comments owner_id
    '''

    req_data = request.get_json()
    comment = CommentModel.get_comment_by_id(comment_id)
    data = comment_schema.dump(comment).data

    if not comment:
        return custom_response({'error': 'comment not found'}, 404)
    
    if request.method == 'PUT':
        if data.get('owner_id') != g.user.get('id'):
            return custom_response({'error': 'permission denied'}, 400)
        
        data, error = comment_schema.load(req_data, partial=True)

        if error:
            return custom_response(error, 400)
        
        comment.update(data)
        data = comment_schema.dump(comment).data
        return custom_response(data, 200)
        
    elif request.method == 'DELETE':
        if data.get('owner_id') != g.user.get('id'):
            return custom_response({'error': 'permission denied'}, 400)
        
        comment.delete()
        return custom_response({'message': 'comment deleted'}, 204)
    
    # GET
    return custom_response(data, 200)
