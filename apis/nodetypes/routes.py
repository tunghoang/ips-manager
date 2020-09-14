from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list nodetypes")
    @api.marshal_list_with(model)
    def get(self):
      '''list nodetypes'''
      return listNodetypes()
    @api.doc('find nodetypes')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find nodetypes'''
      return findNodetype(api.payload)
    @api.doc('new nodetype', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new nodetype'''
      return newNodetype(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get nodetype')
    @api.marshal_with(model)
    def get(self, id):
      '''get nodetype'''
      return getNodetype(id)
    @api.doc('update nodetype', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update nodetype'''
      return updateNodetype(id, api.payload)
    @api.doc('delete nodetype')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete nodetype'''
      return deleteNodetype(id)
    pass