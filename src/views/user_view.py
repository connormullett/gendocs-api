# user_view.py

from flask import request, json, Response, Blueprint
from ..models.user import UserModel, UserSchema
from ..shared.authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()


@user_api.route('/', methods=['POST'])
def register():
    req_data = request.get_json()
    data, error = user_schema.load(req_data)

    if data.get('password') != data.get('confirm_password'):
        return custom_response({'error': 'password mismatch'}, 400)

    if error:
        return custom_response(error, 404)

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
    req_data = request.get_json()

    data, error = user_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)

    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'need email and password to sign in'})

    user = UserModel.get_user_by_email(data.get('email'))

    if not user or not user._check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'})

    ser_data = user_schema.dump(user).data

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'token': token}, 200)


def custom_response(res, status_code):
    return Response(
        mimetype='application/json',
        response=json.dumps(res),
        status=status_code
    )

