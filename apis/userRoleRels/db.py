from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from ..db_utils import DbInstance
from sqlalchemy.exc import *
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

from ..roles import Role
from ..users.user import User
from .userRoleRel import Userrolerel

__db = DbInstance.getInstance()


def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Userrolerel).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Userrolerel).filter(Userrolerel.idUserrolerel == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getUserrolerel(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getUserrolerel(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  queryObj = __db.session().query(
    Userrolerel.idUser, 
    Role.idRole, Role.name, Role.description, 
    User.idUser, User.username
  ).filter(
    Userrolerel.idUser == User.idUser,
    Userrolerel.idRole == Role.idRole
  )
  if 'idUser' in model:
    queryObj = queryObj.filter(Userrolerel.idUser == model['idUser'])
  if 'idRole' in model:
    queryObj = queryObj.filter(Userrolerel.idRole == model['idRole'])
  
  results = queryObj.all()

  return list(map(lambda x: {
    'idUserrolerel': x[0],
    'idRole': x[1],
    'roleName': x[2],
    'roleDescription': x[3],
    'idUser': x[4],
    'username': x[5]
  }, results))

def listUserrolerels():
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

def newUserrolerel(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Userrolerel(model)
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

def getUserrolerel(id):
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

def updateUserrolerel(id, model):
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

def deleteUserrolerel(id):
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

def findUserrolerel(model):
  doLog("find DAO function %s" % model)
  try:
    if 'idRole' in model and 'idUser' in model:
      return {'message': 'put idRole to get list users of the role, put idUser to get lists roles of the user'}
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e
