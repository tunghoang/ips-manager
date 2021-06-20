from sqlalchemy import ForeignKey, Column, Integer, BigInteger, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request
from ..users import User
import os

__db = DbInstance.getInstance()


class Login:
  username = Column(String)
  password = Column(String)

  def __init__(self, dictModel):
    if ("username" in dictModel) and (dictModel["username"] != None):
      self.username = dictModel["username"]
    if ("password" in dictModel) and (dictModel["password"] != None):
      self.password = dictModel["password"]

  def __repr__(self):
    return '<Login username={} password={} >'.format(self.username, self.password, )

  def json(self):
    return {
      "username":self.username,"password":self.password,
    }

  def update(self, dictModel):
    if ("username" in dictModel) and (dictModel["username"] != None):
      self.username = dictModel["username"]
    if ("password" in dictModel) and (dictModel["password"] != None):
      self.password = dictModel["password"]

def __recover():
  pass

def __doList():
  return []
  
def __doNew(instance):
  hash_pw = doHash(str(instance.password))
  user = __db.session().query(User).filter(User.username == instance.username).first()
  if user is None:
    raise BadRequest('No user found')
  elif user.password != hash_pw:
    raise BadRequest('Incorrect password %s %s %s' % (instance.password, hash_pw, user.password))
  else:
    key = doHash(str(instance.username))
    salt = os.urandom(20)
    session[key] = salt
    jwt = doGenJWT(user.json(), salt)
    @after_this_request
    def finalize(response):
      response.set_cookie('key', key)
      response.set_cookie('jwt', jwt)
      response.headers['x-key'] = key
      response.headers['x-jwt'] = jwt
      return response

    return user


def __doUpdate(id, model):
  return {}

def __doDelete(id):
  return {}

def __doFind(model):
  return []


def listLogins():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()
  except InterfaceError as e:
    doLog(e)
    __recover()
    return __doList()
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def newLogin(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Login(model)
  res = False
  try:
    return __doNew(instance)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doNew(instance)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def getLogin(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)
  except InterfaceError as e:
    doLog(e)
    __recover()
    return __doGet(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def updateLogin(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def deleteLogin(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def findLogin(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e
