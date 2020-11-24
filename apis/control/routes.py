from flask_restplus import Resource
from .db import *
from .model import create_status_report

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("dummy api")
    @api.marshal_list_with(model)
    def get(self):
      '''dummy'''
      return listControls()

  @api.route('/<int:id>')
  class Instance(Resource):
    pass

  statusReport = create_status_report(api);

  @api.route('/status/<int:idObject>')
  @api.marshal_with(statusReport)
  class Status(Resource):
    def get(self, idObject):
      '''Get status of idObject'''
      return getStatus(idObject)
