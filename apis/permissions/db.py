from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Permission(__db.Base):
  __tablename__ = "permission"
  idPermission = Column(Integer, primary_key = True)
  idRole = Column(Integer, ForeignKey('role.idRole'))
  idObject = Column(Integer, ForeignKey('object.idObject'))
  action = Column(String(20))

  constraints = list()
  constraints.append(UniqueConstraint('idRole','idObject','action'))
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idPermission" in dictModel) and (dictModel["idPermission"] != None):
      self.idPermission = dictModel["idPermission"]
    if ("idRole" in dictModel) and (dictModel["idRole"] != None):
      self.idRole = dictModel["idRole"]
    if ("idObject" in dictModel) and (dictModel["idObject"] != None):
      self.idObject = dictModel["idObject"]
    if ("action" in dictModel) and (dictModel["action"] != None):
      self.action = dictModel["action"]

  def __repr__(self):
    return '<Permission idPermission={} idRole={} idObject={} action={} >'.format(self.idPermission, self.idRole, self.idObject, self.action, )

  def json(self):
    return {
      "idPermission":self.idPermission,"idRole":self.idRole,"idObject":self.idObject,"action":self.action,
    }

  def update(self, dictModel):
    if ("idPermission" in dictModel) and (dictModel["idPermission"] != None):
      self.idPermission = dictModel["idPermission"]
    if ("idRole" in dictModel) and (dictModel["idRole"] != None):
      self.idRole = dictModel["idRole"]
    if ("idObject" in dictModel) and (dictModel["idObject"] != None):
      self.idObject = dictModel["idObject"]
    if ("action" in dictModel) and (dictModel["action"] != None):
      self.action = dictModel["action"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Permission).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Permission).filter(Permission.idPermission == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getPermission(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getPermission(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Permission).filter_by(**model).all()
  return results


def listPermissions():
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

def newPermission(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Permission(model)
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

def getPermission(id):
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

def updatePermission(id, model):
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

def deletePermission(id):
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

def findPermission(model):
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