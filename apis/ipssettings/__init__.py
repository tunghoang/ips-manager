from .model import create_model
from .routes import init_routes
from .db import Settings
from flask_restplus import Namespace

def create_api():
  api = Namespace('ipssettings', description="ips settings")
  model = create_model(api)
  init_routes(api, model)
  return api