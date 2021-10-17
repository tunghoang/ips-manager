from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list settings")
    @api.marshal_list_with(model)
    def get(self):
      '''list settings'''
      return listSettingss()
    @api.doc('find setting param')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find setting param'''
      return findSettings(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('update setting param', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update setting params'''
      return updateSettings(id, api.payload)
    pass