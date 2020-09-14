from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list roles")
    @api.marshal_list_with(model)
    def get(self):
      '''list roles'''
      return listRoles()
    @api.doc('find role')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find role'''
      return findRole(api.payload)
    @api.doc('new role', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new role'''
      return newRole(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get role')
    @api.marshal_with(model)
    def get(self, id):
      '''get role'''
      return getRole(id)
    @api.doc('update role', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update role'''
      return updateRole(id, api.payload)
    @api.doc('delete role')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete role'''
      return deleteRole(id)
    pass