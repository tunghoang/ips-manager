from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list permissions")
    @api.marshal_list_with(model)
    def get(self):
      '''list permissions'''
      return listPermissions()
    @api.doc('find permissions')
    @api.expect(model)
    #@api.marshal_list_with(model)
    def put(self):
      '''find permissions'''
      return findPermission(api.payload)
    @api.doc('new permission', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new permission'''
      return newPermission(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get permission')
    @api.marshal_with(model)
    def get(self, id):
      '''get permission'''
      return getPermission(id)
    @api.doc('update permission', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update permission'''
      return updatePermission(id, api.payload)
    @api.doc('delete permission')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete permission'''
      return deletePermission(id)
    pass
