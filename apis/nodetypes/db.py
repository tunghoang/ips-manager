from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Nodetype(__db.Base):
  __tablename__ = "nodetype"
  idNodetype = Column(Integer, primary_key = True)
  name = Column(String(50))
  description = Column(String(255))

  def __init__(self, dictModel):
    if ("idNodetype" in dictModel) and (dictModel["idNodetype"] != None):
      self.idNodetype = dictModel["idNodetype"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

  def __repr__(self):
    return '<Nodetype idNodetype={} name={} description={} >'.format(self.idNodetype, self.name, self.description, )

  def json(self):
    return {
      "idNodetype":self.idNodetype,"name":self.name,"description":self.description,
    }

  def update(self, dictModel):
    if ("idNodetype" in dictModel) and (dictModel["idNodetype"] != None):
      self.idNodetype = dictModel["idNodetype"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Nodetype).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Nodetype).filter(Nodetype.idNodetype == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getNodetype(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getNodetype(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Nodetype).filter_by(**model).all()
  return results




def listNodetypes():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()

def newNodetype(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Nodetype(model)
  res = False
  try:
    return __doNew(instance)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doNew(instance)

def getNodetype(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)

def updateNodetype(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)

def deleteNodetype(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)

def findNodetype(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)