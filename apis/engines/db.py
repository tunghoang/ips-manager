from sqlalchemy import ForeignKey, Column, Integer, BigInteger, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Engine(__db.Base):
  __tablename__ = "engine"
  idEngine = Column(Integer, primary_key = True)
  idEnginetype = Column(Integer, ForeignKey('enginetype.idEnginetype'))
  specs = Column(Text)

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idEngine" in dictModel) and (dictModel["idEngine"] != None):
      self.idEngine = dictModel["idEngine"]
    if ("idEnginetype" in dictModel) and (dictModel["idEnginetype"] != None):
      self.idEnginetype = dictModel["idEnginetype"]
    if ("specs" in dictModel) and (dictModel["specs"] != None):
      self.specs = dictModel["specs"]

  def __repr__(self):
    return '<Engine idEngine={} idEnginetype={} specs={} >'.format(self.idEngine, self.idEnginetype, self.specs, )

  def json(self):
    return {
      "idEngine":self.idEngine,"idEnginetype":self.idEnginetype,"specs":self.specs,
    }

  def update(self, dictModel):
    if ("idEngine" in dictModel) and (dictModel["idEngine"] != None):
      self.idEngine = dictModel["idEngine"]
    if ("idEnginetype" in dictModel) and (dictModel["idEnginetype"] != None):
      self.idEnginetype = dictModel["idEnginetype"]
    if ("specs" in dictModel) and (dictModel["specs"] != None):
      self.specs = dictModel["specs"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Engine).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Engine).filter(Engine.idEngine == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getEngine(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getEngine(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Engine).filter_by(**model).all()
  __db.session().commit()
  return results


def listEngines():
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

def newEngine(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Engine(model)
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

def getEngine(id):
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

def updateEngine(id, model):
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

def deleteEngine(id):
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

def findEngine(model):
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