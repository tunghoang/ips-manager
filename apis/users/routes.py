from flask_restplus import Resource
from .db import *
from flask import g

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list users")
    @api.marshal_list_with(model)
    def get(self):
      '''list users'''
      return listUsers()
    @api.doc('find user')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find user'''
      return findUser(api.payload)
    @api.doc('new user', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new user'''
      return newUser(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get user')
    @api.marshal_with(model)
    def get(self, id):
      '''get user'''
      return getUser(id)
    @api.doc('update user', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update user'''
      return updateUser(id, api.payload)
    @api.doc('delete user')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete user'''
      return deleteUser(id)
    pass

  @api.route('/current')
  class CurrentUser(Instance):
    @api.doc("Get current user")
    def get(self):
      roles = getRolesOfUser({'idUser': g.idUser})

      return {
        "idUser": g.idUser,
        "username": g.username,
        "roles": roles}
