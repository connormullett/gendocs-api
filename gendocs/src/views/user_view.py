# user_view.py

from flask import request, json, Response, Blueprint, g
from ..models.user import UserModel, UserSchema
from ..shared.authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()


@user_api.route('/', methods=['POST'])
def register():
    '''
    takes in email: str, name: str, password: str
    creates user and persists to database
    password is hashed for future verification
    returns login token for protected routes
    '''
    req_data = request.get_json()
    data, error = user_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {'error': 'user already exists'}
        return custom_response(message, 400)

    user = UserModel(data)
    user.save()

    ser_data = user_schema.dump(user).data

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'token': token}, 201)


@user_api.route('/login', methods=['POST'])
def login():
    '''
    login route
    body should contain email: str, password: str
    returns token to user for future requests
    on protected routes
    '''
    req_data = request.get_json()

    data, error = user_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)

    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'need email and password to sign in'})

    user = UserModel.get_user_by_email(data.get('email'))

    if not user or not user._check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'}, 400)

    ser_data = user_schema.dump(user).data

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'token': token}, 200)


@user_api.route('/me', methods=['PUT', 'GET', 'DELETE'])
@Auth.auth_required
def me():
    '''
    Handles all actions for 'me',
    users account is stored in g on authentication
    and is pulled to present users data
    '''

    user = UserModel.get_user_by_id(g.user.get('id'))

    if request.method == 'PUT':
        req_data = request.get_json()
        data, error = user_schema.load(req_data, partial=True)

        if error:
            return custom_response(error, 400)

        user.update(data)
        ser_user = user_schema.dump(user).data
        return custom_response(ser_user, 200)

    elif request.method == 'DELETE':
        user.delete()
        return custom_response({'message': 'deleted'}, 204)

    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_user(user_id):
    '''
    URL param -> user_id: int
    returns user data associated from that ID
    '''
    user = UserModel.get_user_by_id(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)

    # TODO: should not return users email and password hash use UserGetDto
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


@user_api.route('/name/<string:name>', methods=['GET'])
@Auth.auth_required
def get_user_by_name(name):
    user = UserModel.get_user_by_name(name)

    if not user:
        return custom_response({'error': 'user not found'}, 404)
    
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)
    

def custom_response(res, status_code):
    '''
    helps with sending Responses from routes
    '''
    return Response(
        mimetype='application/json',
        response=json.dumps(res),
        status=status_code
    )
