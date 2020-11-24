from flask_restplus import Resource
from .db import *
from .model import create_response_model

def init_routes(api, model):
  responseModel = create_response_model(api);
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


  @api.route('/status/<int:idObject>')
  class Status(Resource):
    @api.doc('Node status')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Get status of idObject'''
      return getStatus(idObject)

  @api.route('/start/<int:idObject>')
  class Status(Resource):
    @api.doc('Node start')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Start idObject'''
      return doStart(idObject)

  @api.route('/stop/<int:idObject>')
  class Status(Resource):
    @api.doc('Node stop')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Stop idObject'''
      return doStop(idObject)
