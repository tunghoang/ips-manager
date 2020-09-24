from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request
from ..objects.db import Object

__db = DbInstance.getInstance()



class Containmentrel(__db.Base):
  __tablename__ = "containmentRel"
  idContainmentRel = Column(Integer, primary_key = True)
  idContainer = Column(Integer, ForeignKey('object.idObject'))
  idContainee = Column(Integer, ForeignKey('object.idObject'))

  constraints = list()
  constraints.append(UniqueConstraint('idContainer','idContainee'))
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idContainmentRel" in dictModel) and (dictModel["idContainmentRel"] != None):
      self.idContainmentRel = dictModel["idContainmentRel"]
    if ("idContainer" in dictModel) and (dictModel["idContainer"] != None):
      self.idContainer = dictModel["idContainer"]
    if ("idContainee" in dictModel) and (dictModel["idContainee"] != None):
      self.idContainee = dictModel["idContainee"]

  def __repr__(self):
    return '<Containmentrel idContainmentRel={} idContainer={} idContainee={} >'.format(self.idContainmentRel, self.idContainer, self.idContainee, )

  def json(self):
    return {
      "idContainmentRel":self.idContainmentRel,"idContainer":self.idContainer,"idContainee":self.idContainee,
    }

  def update(self, dictModel):
    if ("idContainmentRel" in dictModel) and (dictModel["idContainmentRel"] != None):
      self.idContainmentRel = dictModel["idContainmentRel"]
    if ("idContainer" in dictModel) and (dictModel["idContainer"] != None):
      self.idContainer = dictModel["idContainer"]
    if ("idContainee" in dictModel) and (dictModel["idContainee"] != None):
      self.idContainee = dictModel["idContainee"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Containmentrel).all()
  
def __doNew(instance):
  __db.session().rollback();
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Containmentrel).filter(Containmentrel.idContainmentrel == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getContainmentrel(id)
  if instance == None:
    return {}
  __db.session().rollback()
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getContainmentrel(id)
  __db.rollback()
  __db.session().delete(instance)
  __db.session().commit()
  return instance

def recursiveFindContainees(model):
  results = __db.session().query(Containmentrel, Object) \
    .filter(Containmentrel.idContainer == model.get('idContainer'), Containmentrel.idContainee == Object.idObject) \
    .with_entities(Object).all()
  results = [r.json() for r in results]
  for r in results:
    res = recursiveFindContainees({'idContainer': r['idObject']})
    if len(res) > 0:
      r['containees'] = res
  return results

def __doFind(model):
  '''
  results = __db.session().query(Containmentrel, Object) \
    .filter(Containmentrel.idContainer == model.get('idContainer'), Containmentrel.idContainee == Object.idObject) \
    .with_entities(Object).all()
  '''
  results = recursiveFindContainees(model)
  return results


def listContainmentrels():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def newContainmentrel(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Containmentrel(model)
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

def getContainmentrel(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def updateContainmentrel(id, model):
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

def deleteContainmentrel(id):
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

def findContainmentrel(model):
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