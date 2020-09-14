from .model import create_model
from .routes import init_routes
from .db import Permission
from flask_restplus import Namespace

def create_api():
  api = Namespace('permissions', description="permission table namespace")
  model = create_model(api)
  init_routes(api, model)
  return api