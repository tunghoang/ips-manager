from sqlalchemy import ForeignKey, Column, Integer, BigInteger, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Rulepackageobjectrel(__db.Base):
  __tablename__ = "rulepackageObjectRel"
  idRulepackageobjectrel = Column(Integer, primary_key = True)
  idRulepackage = Column(Integer, ForeignKey('rulepackage.idRulepackage'))
  idObject = Column(Integer, ForeignKey('object.idObject'))
  errored = Column(Boolean)
  synced = Column(Boolean)
  syncedAt = Column(DateTime)

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idRulepackageobjectrel" in dictModel) and (dictModel["idRulepackageobjectrel"] != None):
      self.idRulepackageobjectrel = dictModel["idRulepackageobjectrel"]
    if ("idRulepackage" in dictModel) and (dictModel["idRulepackage"] != None):
      self.idRulepackage = dictModel["idRulepackage"]
    if ("idObject" in dictModel) and (dictModel["idObject"] != None):
      self.idObject = dictModel["idObject"]
    if ("errored" in dictModel) and (dictModel["errored"] != None):
      self.errored = dictModel["errored"]
    if ("synced" in dictModel) and (dictModel["synced"] != None):
      self.synced = dictModel["synced"]
    if ("syncedAt" in dictModel) and (dictModel["syncedAt"] != None):
      self.syncedAt = dictModel["syncedAt"]

  def __repr__(self):
    return '<Rulepackageobjectrel idRulepackageobjectrel={} idRulepackage={} idObject={} errored={} synced={} syncedAt={} >'.format(self.idRulepackageobjectrel, self.idRulepackage, self.idObject, self.errored, self.synced, self.syncedAt, )

  def json(self):
    return {
      "idRulepackageobjectrel":self.idRulepackageobjectrel,"idRulepackage":self.idRulepackage,"idObject":self.idObject,"errored":self.errored,"synced":self.synced,"syncedAt":self.syncedAt,
    }

  def update(self, dictModel):
    if ("idRulepackageobjectrel" in dictModel) and (dictModel["idRulepackageobjectrel"] != None):
      self.idRulepackageobjectrel = dictModel["idRulepackageobjectrel"]
    if ("idRulepackage" in dictModel) and (dictModel["idRulepackage"] != None):
      self.idRulepackage = dictModel["idRulepackage"]
    if ("idObject" in dictModel) and (dictModel["idObject"] != None):
      self.idObject = dictModel["idObject"]
    if ("errored" in dictModel) and (dictModel["errored"] != None):
      self.errored = dictModel["errored"]
    if ("synced" in dictModel) and (dictModel["synced"] != None):
      self.synced = dictModel["synced"]
    if ("syncedAt" in dictModel) and (dictModel["syncedAt"] != None):
      self.syncedAt = dictModel["syncedAt"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Rulepackageobjectrel).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Rulepackageobjectrel).filter(Rulepackageobjectrel.idRulepackageobjectrel == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getRulepackageobjectrel(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getRulepackageobjectrel(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Rulepackageobjectrel).filter_by(**model).all()
  __db.session().commit()
  return results


def listRulepackageobjectrels():
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

def newRulepackageobjectrel(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Rulepackageobjectrel(model)
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

def getRulepackageobjectrel(id):
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

def updateRulepackageobjectrel(id, model):
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

def deleteRulepackageobjectrel(id):
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

def findRulepackageobjectrel(model):
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