
from flask import request, json, Blueprint, g
from ..models.doc import DocModel, DocSchema, DocType
from .user_view import custom_response

from ..shared.authentication import Auth


doc_api = Blueprint('doc_api', __name__)
doc_schema = DocSchema()


@doc_api.route('/', methods=['POST'])
@Auth.auth_required
def create_doc():
    req_data = request.get_json()
    req_data['owner_id'] = g.user['id']
    data, error = doc_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    doc = DocModel(data)
    doc.save()

    data = doc_schema.dump(doc).data
    return custom_response(data, 201)


@doc_api.route('/<int:doc_id>', methods=['DELETE'])
@Auth.auth_required
def delete(doc_id):
    doc = DocModel.get_doc_by_id(doc_id)

    if not doc:
        return custom_response({'error': 'doc not found'}, 404)

    data = doc_schema.dump(doc).data
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    doc.delete()
    return custom_response({'message': 'deleted'}, 204)


@doc_api.route('/', methods=['GET'])
def get_all():
    docs = DocModel.get_all_docs()
    data = doc_schema.dump(docs, many=True).data
    return custom_response(data, 200)


@doc_api.route('/<int:doc_id>', methods=['GET'])
def get_one(doc_id):
    doc = DocModel.get_doc_by_id(doc_id)

    if not doc:
        return custom_response({'error': 'doc not found'}, 404)

    data = doc_schema.dump(doc).data

    return custom_response(data, 200)


@doc_api.route('/name/<string:doc_name>', methods=['GET'])
def get_one_by_name(doc_name):
    doc = DocModel.get_doc_by_name(doc_name)

    if not doc:
        return custom_response({'error': 'doc not found'}, 404)

    data = doc_schema.dump(doc).data

    return custom_response(data, 200)


@doc_api.route('/<string:doc_type>', methods=['GET'])
def get_docs_by_type(doc_type):
    docs = DocModel.get_docs_by_type(doc_type)

    data = doc_schema.dump(docs, many=True).data
    return custom_response(data, 200)


@doc_api.route('/<int:doc_id>', methods=['PUT'])
@Auth.auth_required
def update(doc_id):
    req_data = request.get_json()
    doc = DocModel.get_doc_by_id(doc_id)

    if not doc:
        return custom_response({'error': 'doc not found'}, 404)

    data = doc_schema.dump(doc).data

    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    data, error = doc_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)

    doc.update(data)
    data = doc_schema.dump(doc).data
    return custom_response(data, 200)


@doc_api.route('/types', methods=['GET'])
def get_doc_types():
    doc_types = DocModel.get_doc_types()

    return custom_response({'types': doc_types}, 200)

