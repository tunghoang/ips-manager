from sqlalchemy import ForeignKey, Column, Integer, BigInteger, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Userrolerel(__db.Base):
  __tablename__ = "userRoleRel"
  idUserRoleRel = Column(Integer, primary_key = True)
  idRole = Column(Integer, ForeignKey('role.idRole'))
  idUser = Column(Integer, ForeignKey('user.idUser'))

  constraints = list()
  constraints.append(UniqueConstraint('idRole','idUser'))
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idUserRoleRel" in dictModel) and (dictModel["idUserRoleRel"] != None):
      self.idUserRoleRel = dictModel["idUserRoleRel"]
    if ("idRole" in dictModel) and (dictModel["idRole"] != None):
      self.idRole = dictModel["idRole"]
    if ("idUser" in dictModel) and (dictModel["idUser"] != None):
      self.idUser = dictModel["idUser"]

  def __repr__(self):
    return '<Userrolerel idUserRoleRel={} idRole={} idUser={} >'.format(self.idUserRoleRel, self.idRole, self.idUser, )

  def json(self):
    return {
      "idUserRoleRel":self.idUserRoleRel,"idRole":self.idRole,"idUser":self.idUser,
    }

  def update(self, dictModel):
    if ("idUserRoleRel" in dictModel) and (dictModel["idUserRoleRel"] != None):
      self.idUserRoleRel = dictModel["idUserRoleRel"]
    if ("idRole" in dictModel) and (dictModel["idRole"] != None):
      self.idRole = dictModel["idRole"]
    if ("idUser" in dictModel) and (dictModel["idUser"] != None):
      self.idUser = dictModel["idUser"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Userrolerel).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Userrolerel).filter(Userrolerel.idUserrolerel == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
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
  results = __db.session().query(Userrolerel).filter_by(**model).all()
  __db.session().commit()
  return results


def listUserrolerels():
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
  except InterfaceError as e:
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
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e