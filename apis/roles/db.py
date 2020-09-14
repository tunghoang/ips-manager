from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Role(__db.Base):
  __tablename__ = "role"
  idRole = Column(Integer, primary_key = True)
  name = Column(String(50))
  description = Column(String(255))

  def __init__(self, dictModel):
    if ("idRole" in dictModel) and (dictModel["idRole"] != None):
      self.idRole = dictModel["idRole"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

  def __repr__(self):
    return '<Role idRole={} name={} description={} >'.format(self.idRole, self.name, self.description, )

  def json(self):
    return {
      "idRole":self.idRole,"name":self.name,"description":self.description,
    }

  def update(self, dictModel):
    if ("idRole" in dictModel) and (dictModel["idRole"] != None):
      self.idRole = dictModel["idRole"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Role).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Role).filter(Role.idRole == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getRole(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getRole(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Role).filter_by(**model).all()
  return results




def listRoles():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()

def newRole(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Role(model)
  res = False
  try:
    return __doNew(instance)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doNew(instance)

def getRole(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)

def updateRole(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)

def deleteRole(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)

def findRole(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)