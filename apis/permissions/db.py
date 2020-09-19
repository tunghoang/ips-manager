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

  constraints = list()
  constraints.append(UniqueConstraint('idRole','idObject'))
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idPermission" in dictModel) and (dictModel["idPermission"] != None):
      self.idPermission = dictModel["idPermission"]
    if ("idRole" in dictModel) and (dictModel["idRole"] != None):
      self.idRole = dictModel["idRole"]
    if ("idObject" in dictModel) and (dictModel["idObject"] != None):
      self.idObject = dictModel["idObject"]

  def __repr__(self):
    return '<Permission idPermission={} idRole={} idObject={} >'.format(self.idPermission, self.idRole, self.idObject, )

  def json(self):
    return {
      "idPermission":self.idPermission,"idRole":self.idRole,"idObject":self.idObject,
    }

  def update(self, dictModel):
    if ("idPermission" in dictModel) and (dictModel["idPermission"] != None):
      self.idPermission = dictModel["idPermission"]
    if ("idRole" in dictModel) and (dictModel["idRole"] != None):
      self.idRole = dictModel["idRole"]
    if ("idObject" in dictModel) and (dictModel["idObject"] != None):
      self.idObject = dictModel["idObject"]

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

def getPermission(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)

def updatePermission(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)

def deletePermission(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)

def findPermission(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)