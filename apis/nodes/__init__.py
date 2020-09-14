from .model import create_model
from .routes import init_routes
from .db import Node
from flask_restplus import Namespace

def create_api():
  api = Namespace('nodes', description="nodes namespace")
  model = create_model(api)
  init_routes(api, model)
  return api