from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Resource(__db.Base):
  __tablename__ = "resource"
  idResource = Column(Integer, primary_key = True)
  name = Column(String(50))
  idNode = Column(Integer, ForeignKey('node.idNode'))
  description = Column(String(255))

  def __init__(self, dictModel):
    if ("idResource" in dictModel) and (dictModel["idResource"] != None):
      self.idResource = dictModel["idResource"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("idNode" in dictModel) and (dictModel["idNode"] != None):
      self.idNode = dictModel["idNode"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

  def __repr__(self):
    return '<Resource idResource={} name={} idNode={} description={} >'.format(self.idResource, self.name, self.idNode, self.description, )

  def json(self):
    return {
      "idResource":self.idResource,"name":self.name,"idNode":self.idNode,"description":self.description,
    }

  def update(self, dictModel):
    if ("idResource" in dictModel) and (dictModel["idResource"] != None):
      self.idResource = dictModel["idResource"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("idNode" in dictModel) and (dictModel["idNode"] != None):
      self.idNode = dictModel["idNode"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Resource).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Resource).filter(Resource.idResource == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getResource(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getResource(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Resource).filter_by(**model).all()
  return results




def listResources():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()

def newResource(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Resource(model)
  res = False
  try:
    return __doNew(instance)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doNew(instance)

def getResource(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)

def updateResource(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)

def deleteResource(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)

def findResource(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)