
import unittest
import os
import json
from gendocs.src.app import create_app, db
from flask import Response
from gendocs.src.views.user_view import custom_response, _check_password


class UserTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.testing = True
        self.client = self.app.test_client
        self.user = {
            'email': 'test@gmail.com',
            'name': 'tester',
            'password': 'Test1!',
            'confirm_password': 'Test1!'
        }

        with self.app.app_context():
            db.create_all()
            self.reg = self.client().post('/v1/users/',
                data=json.dumps(self.user),
                content_type='application/json')
            self.token = self.reg.json['token']
    
    def test_user_registration_should_return_201(self):
        with self.app.app_context():
            self.assertEqual(self.reg.status_code, 201)
    
    def test_bad_user_data_should_return_400(self):
        res = self.client().post(
            '/v1/users/',
            data=json.dumps({'name': 'test'}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)
    
    def test_user_in_db_should_return_400(self):
        res = self.client().post(
            'v1/users/',
            data=self.user,
            content_type='application/json'
        )
        self.assertIn(b'Bad Request', res.data)
        self.assertEqual(res.status_code, 400)
    
    def test_register_password_mismatch_should_return_400(self):
        user = self.user
        user['confirm_password'] = 'test12'
        res = self.client().post(
            'v1/users/',
            data=user,
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_register_bad_password_should_return_400(self):
        '''
        a bad password does not have one of the following:
        symbol, uppercase/lowercase char, numeral
        '''
        user = self.user
        user['password'] = user['confirm_password'] = 'test'

        res = self.client().post(
            'v1/users/',
            data=user,
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)


    def test_register_should_return_token(self):
        self.assertIn('token', self.reg.json)
    
    def test_login_should_return_token(self):
        res = self.client().post(
            'v1/users/login',
            data=json.dumps(self.user),
            content_type='application/json')
        self.assertIn('token', res.json)
    
    def test_login_should_return_404_with_bad_credentials(self):
        res = self.client().post(
            'v1/users/login',
            data=json.dumps({'name': 'test', 'email': 'test@gmail.com', 'password': 'Tester12'}),
            content_type='application/json')
        self.assertIn(b'invalid credentials', res.data)
    
    def test_get_me_should_return_200(self):
        login_res = self.client().post('v1/users/login', data=json.dumps(self.user), content_type='application/json')
        token = login_res.json['token']
        res = self.client().get('v1/users/me', headers={'api-token': token}, content_type='application/json')
        self.assertEqual('tester', res.json.get('name'))
    
    def test_get_me_should_return_400_no_token(self):
        res = self.client().get('v1/users/me')
        self.assertEqual('Authentication token not provided', res.json['error'])
    
    def test_edit_me_should_return_new_user_fields(self):
        edit_res = self.client().put('v1/users/me', data=json.dumps({'name': 'test update'}), headers={'api-token': self.reg.json['token']}, content_type='application/json')
        self.assertEqual(edit_res.status_code, 200)
        self.assertIn(b'update', edit_res.data)
    
    def test_delete_me_should_return_204(self):
        del_res = self.client().delete('v1/users/me', headers={'api-token': self.token}, content_type='application/json')
        self.assertEqual(del_res.status_code, 204)
    
    def test_delete_me_no_users_in_db(self):
        del_res = self.client().delete('v1/users/me', headers={'api-token': self.token}, content_type='application/json')
        res = self.client().get(f'v1/users/by_name/{self.user["name"]}', headers={'api-token': self.token}, content_type='application/json')
        self.assertEqual(res.status_code, 400)  # api-token no longer valid as user was deleted
    
    def test_get_user_by_id(self):
        with self.app.app_context():
            user_id = self.client().get('v1/users/me', headers={'api-token': self.token}, content_type='application/json').json['id']
            res = self.client().get(f'v1/users/by_id/{user_id}', headers={'api-token': self.token}, content_type='application/json')
            self.assertEqual(res.status_code, 200)
        
    def test_get_user_by_name(self):
        with self.app.app_context():
            name = self.client().get('v1/users/me', headers={'api-token': self.token}, content_type='application/json').json['name']
            res = self.client().get(f'v1/users/by_name/{name}', headers={'api-token': self.token}, content_type='application/json')
            self.assertEqual(res.status_code, 200)
    
    def test_custom_response_should_return_custom_response(self):
        self.c_res = custom_response({'status': 'this should work'}, 200)
        self.assertIsInstance(self.c_res, Response)
    
    def test_check_password_should_return_true_for_good_password(self):
        password = self.user['password']
        self.assertTrue(_check_password(password))

    def test_check_password_should_return_false_for_bad_password(self):
        password = 'test'
        self.assertFalse(_check_password(password))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
