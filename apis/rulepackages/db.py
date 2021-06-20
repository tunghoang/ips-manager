from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Rulepackage(__db.Base):
  __tablename__ = "rulepackage"
  idRulepackage = Column(Integer, primary_key = True)
  idEnginetype = Column(Integer, ForeignKey('enginetype.idEnginetype'))
  application = Column(String(100))
  version = Column(BigInteger)
  appliedAt = Column(DateTime)
  status = Column(String(50))

  constraints = list()
  constraints.append(UniqueConstraint('idEnginetype','application','version'))
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idRulepackage" in dictModel) and (dictModel["idRulepackage"] != None):
      self.idRulepackage = dictModel["idRulepackage"]
    if ("idEnginetype" in dictModel) and (dictModel["idEnginetype"] != None):
      self.idEnginetype = dictModel["idEnginetype"]
    if ("application" in dictModel) and (dictModel["application"] != None):
      self.application = dictModel["application"]
    if ("version" in dictModel) and (dictModel["version"] != None):
      self.version = dictModel["version"]
    if ("appliedAt" in dictModel) and (dictModel["appliedAt"] != None):
      self.appliedAt = dictModel["appliedAt"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]

  def __repr__(self):
    return '<Rulepackage idRulepackage={} idEnginetype={} application={} version={} appliedAt={} status={} >'.format(self.idRulepackage, self.idEnginetype, self.application, self.version, self.appliedAt, self.status, )

  def json(self):
    return {
      "idRulepackage":self.idRulepackage,"idEnginetype":self.idEnginetype,"application":self.application,"version":self.version,"appliedAt":self.appliedAt,"status":self.status,
    }

  def update(self, dictModel):
    if ("idRulepackage" in dictModel) and (dictModel["idRulepackage"] != None):
      self.idRulepackage = dictModel["idRulepackage"]
    if ("idEnginetype" in dictModel) and (dictModel["idEnginetype"] != None):
      self.idEnginetype = dictModel["idEnginetype"]
    if ("application" in dictModel) and (dictModel["application"] != None):
      self.application = dictModel["application"]
    if ("version" in dictModel) and (dictModel["version"] != None):
      self.version = dictModel["version"]
    if ("appliedAt" in dictModel) and (dictModel["appliedAt"] != None):
      self.appliedAt = dictModel["appliedAt"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Rulepackage).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Rulepackage).filter(Rulepackage.idRulepackage == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getRulepackage(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getRulepackage(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Rulepackage).filter_by(**model).all()
  __db.session().commit()
  return results


def listRulepackages():
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

def newRulepackage(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Rulepackage(model)
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

def getRulepackage(id):
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

def updateRulepackage(id, model):
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

def deleteRulepackage(id):
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

def findRulepackage(model):
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