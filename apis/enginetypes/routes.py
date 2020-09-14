from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list enginetypes")
    @api.marshal_list_with(model)
    def get(self):
      '''list enginetypes'''
      return listEnginetypes()
    @api.doc('find enginetypes')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find enginetypes'''
      return findEnginetype(api.payload)
    @api.doc('new enginetype', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new enginetype'''
      return newEnginetype(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get enginetype')
    @api.marshal_with(model)
    def get(self, id):
      '''get enginetype'''
      return getEnginetype(id)
    @api.doc('update enginetype', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update enginetype'''
      return updateEnginetype(id, api.payload)
    @api.doc('delete enginetype')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete enginetype'''
      return deleteEnginetype(id)
    pass