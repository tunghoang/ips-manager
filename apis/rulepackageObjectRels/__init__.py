from .model import create_model
from .routes import init_routes
from .db import Rulepackageobjectrel
from flask_restplus import Namespace

def create_api():
  api = Namespace('rulepackageObjectRels', description="rulepackageObjectRels table namespace")
  model = create_model(api)
  init_routes(api, model)
  return api