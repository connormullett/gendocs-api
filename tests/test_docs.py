
import os
import tempfile

import pytest, unittest

from ..src import create_app

class TestDocs(unittest.TestCase):

    def setUp(self):
        print(create_app)

# @pytest.fixture
# def client():
#     app = create_app('testing')
