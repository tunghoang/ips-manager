from .model import create_model
from .routes import init_routes
from .db import Engine
from flask_restplus import Namespace

def create_api():
  api = Namespace('engines', description="engines namespace")
  model = create_model(api)
  init_routes(api, model)
  return api