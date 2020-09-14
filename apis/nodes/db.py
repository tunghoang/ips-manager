from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Node(__db.Base):
  __tablename__ = "node"
  idNode = Column(Integer, primary_key = True)
  idNodetype = Column(Integer, ForeignKey('nodetype.idNodetype'))
  specs = Column(Text)

  def __init__(self, dictModel):
    if ("idNode" in dictModel) and (dictModel["idNode"] != None):
      self.idNode = dictModel["idNode"]
    if ("idNodetype" in dictModel) and (dictModel["idNodetype"] != None):
      self.idNodetype = dictModel["idNodetype"]
    if ("specs" in dictModel) and (dictModel["specs"] != None):
      self.specs = dictModel["specs"]

  def __repr__(self):
    return '<Node idNode={} idNodetype={} specs={} >'.format(self.idNode, self.idNodetype, self.specs, )

  def json(self):
    return {
      "idNode":self.idNode,"idNodetype":self.idNodetype,"specs":self.specs,
    }

  def update(self, dictModel):
    if ("idNode" in dictModel) and (dictModel["idNode"] != None):
      self.idNode = dictModel["idNode"]
    if ("idNodetype" in dictModel) and (dictModel["idNodetype"] != None):
      self.idNodetype = dictModel["idNodetype"]
    if ("specs" in dictModel) and (dictModel["specs"] != None):
      self.specs = dictModel["specs"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Node).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Node).filter(Node.idNode == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getNode(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getNode(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Node).filter_by(**model).all()
  return results




def listNodes():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()

def newNode(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Node(model)
  res = False
  try:
    return __doNew(instance)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doNew(instance)

def getNode(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)

def updateNode(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)

def deleteNode(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)

def findNode(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)