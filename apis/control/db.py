from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

import json
from ..objects import Object
from ..engines import Engine

__db = DbInstance.getInstance()


class Control:
  dummy = Column(Integer)

  def __init__(self, dictModel):
    if ("dummy" in dictModel) and (dictModel["dummy"] != None):
      self.dummy = dictModel["dummy"]

  def __repr__(self):
    return '<Control dummy={} >'.format(self.dummy, )

  def json(self):
    return {
      "dummy":self.dummy,
    }

  def update(self, dictModel):
    if ("dummy" in dictModel) and (dictModel["dummy"] != None):
      self.dummy = dictModel["dummy"]

def __recover():
  pass

def __doList():
  return []
  
def __doNew(instance):
  return {}

def __doUpdate(id, model):
  return {}

def __doDelete(id):
  return {}

def __doFind(model):
  return []


def listControls():
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

def newControl(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Control(model)
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

def getControl(id):
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

def updateControl(id, model):
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

def deleteControl(id):
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

def findControl(model):
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

def getEngineSpecs(idObject):
  try:
    results = __db.session().query(
      Object.name, 
      Engine.specs
    ).filter(
      Object.idEngine == Engine.idEngine,
      Object.idObject == idObject
    ).all()
    if len(results) > 0:
      doLog(results[0][1])
      return json.loads(results[0][1])
    else:
      return None
  except OperationalError as e:
    doLog(e)
    __recover()
    return getEngineSpecs(idObject)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def getStatus(idObject):
  doLog('ggggetStatus ' + str(idObject))
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      # prob for status
      success, data = make_get_request(specs['endpoint'], '/engine/status')
      resData = json.loads(data)
      if success:
        return {'success': resData['status']['code'] == 200, 'online': resData['data']['engine_status'] == 'Running\n', 'enabled': True, 'data': data}
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    return {'success': False, 'data': str(e)}

def doStart(idObject):
  doLog('doStart ', idObject)
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      # prob for status
      success, data = make_get_request(specs['endpoint'], '/engine/start')
      resData = json.loads(data)
      doLog(resData)
      if success:
        return {'success': resData['status']['code'] == 200, 'online': resData['data']['status'], 'enabled': True, 'data': data}
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def doStop(idObject):
  doLog('doStop ', idObject)
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      # prob for status
      success, data = make_get_request(specs['endpoint'], '/engine/stop')
      resData = json.loads(data)
      doLog(resData)
      if success:
        return {'success': resData['status']['code'] == 200, 'online': not resData['data']['status'], 'enabled': True, 'data': data}
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}
