from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list objects")
    @api.marshal_list_with(model)
    def get(self):
      '''list objects'''
      return listObjects()
    @api.doc('find objects')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find objects'''
      return findObject(api.payload)
    @api.doc('new object', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new object'''
      return newObject(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get object')
    @api.marshal_with(model)
    def get(self, id):
      '''get object'''
      return getObject(id)
    @api.doc('update object', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update object'''
      return updateObject(id, api.payload)
    @api.doc('delete object')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete object'''
      return deleteObject(id)
    pass