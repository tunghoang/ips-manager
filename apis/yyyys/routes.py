from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list resources")
    @api.marshal_list_with(model)
    def get(self):
      '''list resources'''
      return listYyyys()
    @api.doc('find resources')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find resources'''
      return findYyyy(api.payload)
    @api.doc('new resource', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new resource'''
      return newYyyy(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get resource')
    @api.marshal_with(model)
    def get(self, id):
      '''get resource'''
      return getYyyy(id)
    @api.doc('update resource', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update resource'''
      return updateYyyy(id, api.payload)
    @api.doc('delete resource')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete resource'''
      return deleteYyyy(id)
    pass