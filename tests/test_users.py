
import unittest
import os
import json
from gendocs.src.app import create_app, db


class UserTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.testing = True
        self.client = self.app.test_client
        self.user = {
            'email': 'test@gmail.com',
            'name': 'tester',
            'password': 'test'
        }

        with self.app.app_context():
            db.create_all()
    
    def test_user_registration_should_return_201(self):
        res = self.client().post('/v1/users/',
            data=json.dumps(self.user),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
    
    def test_bad_user_data_should_return_400(self):
        res = self.client().post(
            '/v1/users/',
            data=json.dumps({'name': 'test'}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)
    
    def test_user_in_db_should_return_400(self):
        self.client().post(
            'v1/users/',
            data = self.user,
            content_type='application/json'
        )
        res = self.client().post(
            'v1/users/',
            data=self.user,
            content_type='application/json'
        )
        self.assertIn(b'Bad Request', res.data)
        self.assertEqual(res.status_code, 400)
    
    def test_register_should_return_token(self):
        res = self.client().post(
            'v1/users/',
            data=json.dumps({'name': 'test', 'email': 'test@gmail.com', 'password': 'test'}),
            content_type='application/json'
        )
        self.assertIn(b'token', res.data)
    
    def test_login_should_return_token(self):
        with self.client().post('v1/users/',
          data=json.dumps({'name': 'test', 'email': 'test@gmail.com', 'password': 'test'}),
          content_type='application/json'):
            res = self.client().post(
                'v1/users/login',
                data=json.dumps({'name': 'test', 'email': 'test@gmail.com', 'password': 'test'}),
                content_type='application/json')
            self.assertIn(b'token', res.data)
    
    def test_login_should_return_404_with_bad_credentials(self):
        with self.client().post('v1/users/',
          data=json.dumps({'name': 'test', 'email': 'test@gmail.com', 'password': 'test'}),
          content_type='application/json'):
            res = self.client().post(
                'v1/users/login',
                data=json.dumps({'name': 'test', 'email': 'test@gmail.com', 'password': 'tester12'}),
                content_type='application/json')
            self.assertIn(b'invalid credentials', res.data)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
