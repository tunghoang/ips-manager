from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("check login")
    @api.marshal_list_with(model)
    def get(self):
      '''check login'''
      return listLogins()
    @api.doc('do login', body=model)
    @api.expect(model)
    # @api.marshal_with(model)
    def post(self):
      '''do login'''
      return newLogin(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    pass