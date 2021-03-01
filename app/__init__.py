from flask_restplus import Api
from flask import Blueprint

from main.controller.parse_controller import api as parse_ns
from main.controller.edge_detection_controller import api as edge_detector_ns


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='tinvois receipt parser',
          version='1.0',
          description='tinvois receipt parser'
          )

api.add_namespace(parse_ns, path='/parse')
api.add_namespace(edge_detector_ns, path='/detect_edges')
