from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list all rulepackageObjectRels")
    @api.marshal_list_with(model)
    def get(self):
      '''list all rulepackageObjectRel'''
      return listRulepackageobjectrels()
    @api.doc('find rulepackageObjectRel')
    @api.expect(model)
    def put(self):
      '''find rulepackageObjectRel'''
      return findRulepackageobjectrel(api.payload)
    @api.doc('create new rulepackageObjectRel', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create new rulepackageObjectRel'''
      return newRulepackageobjectrel(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('delete rulepackageObjectRel')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete rulepackageObjectRel'''
      return deleteRulepackageobjectrel(id)
    pass
