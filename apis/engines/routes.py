from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list engines")
    #@api.marshal_list_with(model)
    def get(self):
      '''list engines'''
      return listEngines()
    @api.doc('find engines')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find engines'''
      return findEngine(api.payload)
    @api.doc('new engine', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new engine'''
      return newEngine(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get engine')
    @api.marshal_with(model)
    def get(self, id):
      '''get engine'''
      return getEngine(id)
    @api.doc('update engine', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update engine'''
      return updateEngine(id, api.payload)
    @api.doc('delete engine')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete engine'''
      return deleteEngine(id)
    pass
