
from flask import jsonify, request, g, Blueprint
from ..models.reply import ReplyModel, ReplySchema
from .user_view import custom_response

from ..shared.authentication import Auth

reply_api = Blueprint('reply_api', __name__)
reply_schema = ReplySchema()


@reply_api.route('/', methods=['POST'])
@Auth.auth_required
def create_reply():
    req_data = request.get_json()
    req_data['owner_id'] = g.user['id']
    data, error = reply_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    reply = ReplyModel(data)
    reply.save()

    data = reply_schema.dump(reply).data
    return custom_response(data, 201)


@reply_api.route('/<int:reply_id>', methods=['GET'])
def get_reply_by_id(reply_id):
    replies = ReplyModel.get_reply_by_id(reply_id)
    data = reply_schema.dump(replies).data
    return custom_response(data, 200)


@reply_api.route('/<int:reply_id>', methods=['PUT', 'DELETE'])
@Auth.auth_required
def edit_delete_reply(reply_id):

    req_data = request.get_json()
    reply = ReplyModel.get_reply_by_id(reply_id)

    if not reply:
        return custom_response({'error': 'reply not found'}, 404)
    
    data, error = reply_schema.load(req_data, partial=True)

    if error:
        return custom(error, 400)

    if request.method == 'PUT':
        reply.update(data)
        data = reply_schema.dump(reply).data
        return custom_response(data, 200)
    elif request.method == 'DELETE':
        reply.delete()
        return custom_response({'message': 'deleted'}, 204)


@reply_api.route('/by_comment/<int:comment_id>')
def get_replies_by_comment_id(comment_id):
    replies = ReplyModel.get_replies_by_comment_id(comment_id)
    data = reply_schema.dump(replies, many=True).data
    return custom_response(data, 200)
