from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list user-role relationships")
    @api.marshal_list_with(model)
    def get(self):
      '''list user-role relationships'''
      return listUserrolerels()
    @api.doc('find user-role relationships')
    @api.expect(model)
    # @api.marshal_list_with(model)  # TUNG
    # @api.marshal_list_with(roleModel)
    def put(self):
      '''find user-role relationships'''
      return findUserrolerel(api.payload)

    @api.doc('assign role to a user', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''assign a role to a user'''
      return newUserrolerel(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get a user-role rels')
    @api.marshal_with(model)
    def get(self, id):
      '''get user'''
      return getUserrolerel(id)
    @api.doc('update', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update'''
      return updateUserrolerel(id, api.payload)
    @api.doc('delete')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete'''
      return deleteUserrolerel(id)
    pass