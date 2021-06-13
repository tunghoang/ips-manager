from flask import request
from flask_restplus import Resource
from .db import *

zipPath = '../ansible/files/zips'
def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list applied rulepackages")
    @api.marshal_list_with(model)
    def get(self):
      '''list applied rulepackages'''
      return listRulepackages()
    @api.doc('create a new rulepackage', body=model)
    #@api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create a new rulepackage for applied'''
      payload = request.form.to_dict()
      zipfile = request.files.get('zipfile')
      print(payload)
      print(files)
      fname = f"{zipPath}/ruleset-{payload['application']}-{payload['version']}.zip"
      zipfile.save(fname)
      return {'message': 'hello world'}
      #return newRulepackage(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('delete an existing rulepackage')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete an existing rulepackage'''
      return deleteRulepackage(id)
    pass
