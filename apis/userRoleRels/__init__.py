from .model import create_model
from .routes import init_routes
from .db import Userrolerel
from flask_restplus import Namespace

def create_api():
  api = Namespace('userRoleRels', description="User-Role relationship (many - many)")
  model = create_model(api)
  init_routes(api, model)
  return api