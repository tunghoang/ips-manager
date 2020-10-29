from .model import create_model
from .routes import init_routes
from .role import Role
from flask_restplus import Namespace

def create_api():
  api = Namespace('roles', description="roles namespace")
  model = create_model(api)
  init_routes(api, model)
  return api