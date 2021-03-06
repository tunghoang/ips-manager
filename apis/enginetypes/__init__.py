from .model import create_model
from .routes import init_routes
from .db import Enginetype
from flask_restplus import Namespace

def create_api():
  api = Namespace('enginetypes', description="engine types (hostIPS, netIPS)")
  model = create_model(api)
  init_routes(api, model)
  return api