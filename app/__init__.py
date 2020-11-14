from flask_restplus import Api
from flask import Blueprint

from app.main.controller.parse_controller import api as parse_ns


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='tinvois receipt parser',
          version='1.0',
          description='tinvois receipt parser'
          )

api.add_namespace(parse_ns, path='/parse')
