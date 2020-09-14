from .model import create_model
from .routes import init_routes
from .db import Nodetype
from flask_restplus import Namespace

def create_api():
  api = Namespace('nodetypes', description="node types (hostIPS, netIPS)")
  model = create_model(api)
  init_routes(api, model)
  return api