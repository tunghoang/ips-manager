from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

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
  return {}

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

def getLogin(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)

def updateLogin(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)

def deleteLogin(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)

def findLogin(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)