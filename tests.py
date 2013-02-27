import os
os.environ['WEB_ENV'] = 'test'

import unittest

import web
from web.browser import AppBrowser

from app import app

b = AppBrowser(app)

class AppTest(unittest.TestCase):
    def setUp(self):
        # Add global setup here
        pass

class TestIntegration(AppTest):
    def test_index(self):
        b.open('/')
        self.assertEqual(200, b.status)

if __name__ == '__main__':
    unittest.main()
