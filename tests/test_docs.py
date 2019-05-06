
import unittest
import os
import json
from gendocs.src.app import create_app, db


class UserTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.user = {
            'email': 'test@gmail.com',
            'name': 'tester',
            'password': 'test'
        }

        with self.app.app_context():
            db.create_all()
    
    def test_user_registration_should_return_201(self):
        res = self.client().post('/v1/users/', data=self.user)
        self.assertEqual(res.status_code, 201)
