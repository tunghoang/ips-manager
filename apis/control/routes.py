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
  class Start(Resource):
    @api.doc('Node start')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Start idObject'''
      return doStart(idObject)

  @api.route('/stop/<int:idObject>')
  class Stop(Resource):
    @api.doc('Node stop')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Stop idObject'''
      return doStop(idObject)

  @api.route('/ansStartBeats/<int:idObject>')
  class AnsStart(Resource):
    @api.doc('Ansible start beats')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Ansible start beats'''
      return ansStartBeats(idObject)

  @api.route('/ansStopBeats/<int:idObject>')
  class AnsStop(Resource):
    @api.doc('Ansible stop beats')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Ansible start beats'''
      return ansStopBeats(idObject)

  @api.route('/ansStartIPS/<int:idObject>')
  class AnsStartIPS(Resource):
    @api.doc('Ansible start beats')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Ansible start IPS'''
      return ansStartIPS(idObject)

  @api.route('/ansStopIPS/<int:idObject>')
  class AnsStopIPS(Resource):
    @api.doc('Ansible stop IPS')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Ansible stop IPS'''
      return ansStopIPS(idObject)

  @api.route('/ansStart/<int:idObject>')
  class AnsStartIPS(Resource):
    @api.doc('Ansible start')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Ansible start IPS'''
      return ansStart(idObject)

  @api.route('/ansStop/<int:idObject>')
  class AnsStopIPS(Resource):
    @api.doc('Ansible stop')
    @api.marshal_with(responseModel)
    def get(self, idObject):
      '''Ansible stop IPS'''
      return ansStop(idObject)

  @api.route('/query/webservers/<int:idObject>')
  class QueryWebservers(Resource):
    @api.doc("query webserver of node")
    def get(self, idObject):
      '''Query webserver of node with Id'''
      return queryWebservers(idObject)

  @api.route('/query/modsec-rules/<int:idObject>')
  class QueryModSecRules(Resource):
    @api.doc("query webserver of node")
    def get(self, idObject):
      '''Query webserver of node with Id'''
      return queryModSecRules(idObject)

  @api.route('/ruleset/<int:idObject>')
  class RulesetInstaller(Resource):
    @api.doc("Install ruleset for idObject")
    def post(self, idObject):
      webserver = api.payload['webserver']
      ruleset = api.payload['ruleset']
      return installRuleset(idObject, webserver, ruleset)
    def delete(self, idObject):
      webserver = api.payload['webserver']
      ruleset = api.payload['ruleset']
      return uninstallRuleset(idObject, webserver, ruleset)

  @api.route('/watchList/<int:idObject>')
  class WatchList(Resource):
    @api.doc("Get list of watched directories")
    def get(self, idObject):
      return getWatchList(idObject)
    @api.doc("Update list of watched directories")
    def put(self, idObject):
      watchList = api.payload
      return updateWatchList(idObject, watchList)
