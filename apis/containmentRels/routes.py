from flask_restplus import Resource
from .db import *
from flask_restplus import fields

def init_routes(api, model):
  containee = api.model('containee', {
    'idObject': fields.Integer,
    'name': fields.String,
    'idEngine': fields.Integer,
    'description': fields.String,
    'containees': fields.List(fields.Raw)
  },mask='*')
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list containment relationships")
    @api.marshal_list_with(model)
    def get(self):
      '''list containment relationships'''
      return listContainmentrels()
    @api.doc('find containment relationships')
    @api.expect(model)
    @api.marshal_list_with(containee)
    def put(self):
      '''find containment relationships'''
      return findContainmentrel(api.payload)
    @api.doc('new containment relationship', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new containment relationship'''
      return newContainmentrel(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get a containment relationship')
    @api.marshal_with(model)
    def get(self, id):
      '''get a containment relationship'''
      return getContainmentrel(id)
    @api.doc('update a containment relationship', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update a containment relationship'''
      return updateContainmentrel(id, api.payload)
    @api.doc('delete containment relationship')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete containment relationship'''
      return deleteContainmentrel(id)
    pass