from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

from ..roles import Role
from ..objects import Object

__db = DbInstance.getInstance()



class Permission(__db.Base):
  __tablename__ = "permission"
  idPermission = Column(Integer, primary_key = True)
  idRole = Column(Integer, ForeignKey('role.idRole', ondelete="CASCADE"))
  idObject = Column(Integer, ForeignKey('object.idObject', ondelete="CASCADE"))
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
  result = __db.session().query(Permission).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Permission).filter(Permission.idPermission == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
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
  queryObj = __db.session().query(
    Permission.idPermission, Permission.action,
    Role.idRole, Role.name, Role.description,
    Object.idObject, Object.name, Object.description, Object.idEngine
  ).filter(
    Permission.idRole == Role.idRole,
    Permission.idObject == Object.idObject
  )

  if 'idRole' in model:
    queryObj = queryObj.filter(Permission.idRole == model['idRole'])

  if 'idObject' in model:
    queryObj = queryObj.filter(Permission.idObject == model['idObject'])

  results = queryObj.all()
  l = list(map(lambda x: {
    'idPermission': x[0],
    'action': x[1],
    'idRole': x[2],
    'roleName': x[3],
    'roleDescription': x[4],
    'idObject': x[5],
    'objectName': x[6],
    'objectDescription': x[7],
    'idEngine': x[8]
  },results))
  doLog(l)

  queryObj1 = __db.session().query(
    Permission.idPermission, Permission.action, 
    Role.idRole, Role.name, Role.description, Permission.idObject 
  ).filter(
    Permission.idRole == Role.idRole,
    Permission.idObject == None
  )

  if 'idRole' in model:
    queryObj1 = queryObj1.filter(Permission.idRole == model['idRole'])

  results1 = queryObj1.all()

  __db.session().commit()

  l1 = list(map(lambda x: {
    'idPermission': x[0],
    'action': x[1],
    'idRole': x[2],
    'roleName': x[3],
    'roleDescription': x[4],
    'idObject': x[5],
    'objectName': None,
    'objectDescription': None,
    'idEngine': None
  },results1))
  doLog("Haahahahaha")
  doLog(l1)
  return l1 + l

def listPermissions():
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
  except InterfaceError as e:
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
