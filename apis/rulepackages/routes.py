from flask import request, current_app
from flask_restplus import Resource
from werkzeug.exceptions import *
from .db import *
from datetime import datetime
import os

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list applied rulepackages")
    @api.marshal_list_with(model)
    def get(self):
      '''list applied rulepackages'''
      zipPath = os.path.join(current_app.root_path, 'files/zips')
      print(current_app.root_path)
      print(f'zipPath: {zipPath}')
      return listRulepackages()
    @api.doc('create a new rulepackage', body=model)
    #@api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create a new rulepackage for applied'''
      payload = request.form.to_dict()
      payload['appliedAt'] = datetime.now()
      payload['status'] = 'uploaded'
      datafile = request.files.get('datafile')
      print(payload)
      print(datafile)
      zipPath = os.path.join(current_app.root_path, 'files/zips')
      path = f"{zipPath}/{payload['application']}/{payload['version']}"
      if not os.path.exists(path):
        os.makedirs(path, 0o755)
      
      fname = f"{path}/ruleset-{payload['application']}-{payload['version']}.{payload['fileExt']}"
      datafile.save(fname)
      return newRulepackage(payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('delete an existing rulepackage')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete an existing rulepackage'''
      try:
        return deleteRulepackage(id)
      except Exception as e:
        raise BadRequest(str(e))
    pass
