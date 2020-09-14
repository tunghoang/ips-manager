from .model import create_model
from .routes import init_routes
from .db import Containmentrel
from flask_restplus import Namespace

def create_api():
  api = Namespace('containmentRels', description="containment relationships. This will implement grouping capability")
  model = create_model(api)
  init_routes(api, model)
  return api