from flask_testing import TestCase
from app.manage import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        return app
