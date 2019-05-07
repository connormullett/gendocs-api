
import unittest
import os
import json
from gendocs.src.app import create_app, db


class DocTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.testing = True
        self.client = self.app.test_client
        self.user = {
            'email': 'test@gmail.com',
            'name': 'tester',
            'password': 'test'
        }
        self.doc = {
            'title': 'title',
            'content': 'content',
            'language': 'Python',
            'doc_type': 'TUTORIAL'
        }

        with self.app.app_context():
            db.create_all()
            self.reg = self.client().post('v1/users/',
                data=json.dumps(self.user),
                content_type='application/json')
            self.token = self.reg.json['token']
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
