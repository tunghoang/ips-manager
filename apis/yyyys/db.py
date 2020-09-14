from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Yyyy(__db.Base):
  __tablename__ = "yyyy"
  idYyyy = Column(Integer, primary_key = True)
  name = Column(String(50))
  idNode = Column(Integer, ForeignKey('node.idNode'))
  description = Column(String(255))

  def __init__(self, dictModel):
    if ("idYyyy" in dictModel) and (dictModel["idYyyy"] != None):
      self.idYyyy = dictModel["idYyyy"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("idNode" in dictModel) and (dictModel["idNode"] != None):
      self.idNode = dictModel["idNode"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

  def __repr__(self):
    return '<Yyyy idYyyy={} name={} idNode={} description={} >'.format(self.idYyyy, self.name, self.idNode, self.description, )

  def json(self):
    return {
      "idYyyy":self.idYyyy,"name":self.name,"idNode":self.idNode,"description":self.description,
    }

  def update(self, dictModel):
    if ("idYyyy" in dictModel) and (dictModel["idYyyy"] != None):
      self.idYyyy = dictModel["idYyyy"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("idNode" in dictModel) and (dictModel["idNode"] != None):
      self.idNode = dictModel["idNode"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Yyyy).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Yyyy).filter(Yyyy.idYyyy == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getYyyy(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getYyyy(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Yyyy).filter_by(**model).all()
  return results




def listYyyys():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()

def newYyyy(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Yyyy(model)
  res = False
  try:
    return __doNew(instance)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doNew(instance)

def getYyyy(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)

def updateYyyy(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)

def deleteYyyy(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)

def findYyyy(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)