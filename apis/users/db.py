from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class User(__db.Base):
  __tablename__ = "user"
  idUser = Column(Integer, primary_key = True)
  username = Column(String(50))
  password = Column(String(100))

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idUser" in dictModel) and (dictModel["idUser"] != None):
      self.idUser = dictModel["idUser"]
    if ("username" in dictModel) and (dictModel["username"] != None):
      self.username = dictModel["username"]
    if ("password" in dictModel) and (dictModel["password"] != None):
      self.password = dictModel["password"]

  def __repr__(self):
    return '<User idUser={} username={} password={} >'.format(self.idUser, self.username, self.password, )

  def json(self):
    return {
      "idUser":self.idUser,"username":self.username,"password":self.password,
    }

  def update(self, dictModel):
    if ("idUser" in dictModel) and (dictModel["idUser"] != None):
      self.idUser = dictModel["idUser"]
    if ("username" in dictModel) and (dictModel["username"] != None):
      self.username = dictModel["username"]
    if ("password" in dictModel) and (dictModel["password"] != None):
      self.password = dictModel["password"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(User).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(User).filter(User.idUser == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getUser(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getUser(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(User).filter_by(**model).all()
  return results


def listUsers():
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

def newUser(model):
  doLog("new DAO function. model: {}".format(model))
  instance = User(model)
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

def getUser(id):
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

def updateUser(id, model):
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

def deleteUser(id):
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

def findUser(model):
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