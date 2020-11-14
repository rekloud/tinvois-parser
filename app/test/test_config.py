import os
import unittest

from flask import current_app
from flask_testing import TestCase

from app.manage import app
from app.main.config import basedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        return app

    def test_app_is_development(self):
        pass


if __name__ == '__main__':
    unittest.main()
