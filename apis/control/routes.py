from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("dummy api")
    @api.marshal_list_with(model)
    def get(self):
      '''dummy'''
      return listControls()

  @api.route('/<int:id>')
  class Instance(Resource):
    pass