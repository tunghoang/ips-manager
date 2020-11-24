from .model import create_model
from .routes import init_routes
from .db import Control
from flask_restplus import Namespace

def create_api():
  api = Namespace('control', description="node controls")
  model = create_model(api)
  init_routes(api, model)
  return api