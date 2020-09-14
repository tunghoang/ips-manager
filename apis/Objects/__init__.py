from .model import create_model
from .routes import init_routes
from .db import Object
from flask_restplus import Namespace

def create_api():
  api = Namespace('Objects', description="objects can be nodes or groups")
  model = create_model(api)
  init_routes(api, model)
  return api