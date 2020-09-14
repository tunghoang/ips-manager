from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list nodes")
    @api.marshal_list_with(model)
    def get(self):
      '''list nodes'''
      return listNodes()
    @api.doc('find nodes')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find nodes'''
      return findNode(api.payload)
    @api.doc('new node', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new node'''
      return newNode(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get node')
    @api.marshal_with(model)
    def get(self, id):
      '''get node'''
      return getNode(id)
    @api.doc('update node', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update node'''
      return updateNode(id, api.payload)
    @api.doc('delete node')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete node'''
      return deleteNode(id)
    pass