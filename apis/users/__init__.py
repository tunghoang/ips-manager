from .model import create_model
from .routes import init_routes
from .user import User
from flask_restplus import Namespace

def create_api():
  api = Namespace('users', description="users namespace")
  model = create_model(api)
  init_routes(api, model)
  return api