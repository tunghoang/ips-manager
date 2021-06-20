import traceback
from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from ..db_helper import getEngineSpecs

from werkzeug.exceptions import *
from flask import session,request,after_this_request

import json

from ..ansible_utils import provision,stopBeats,startBeats,stopIPS,startIPS, installModSecRules, uninstallModSecRules

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
  except InterfaceError as e:
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
  doLog("get DAO function " + str(id))
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
  doLog("delete DAO function " + str(id))
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

def __get_ip_from_specs(specs):
  return specs['hostname']
  
def __getEngineIP(idObject):
  specs = getEngineSpecs(idObject)
  if specs is None:
    return None
  return __get_ip_from_specs( specs )

def getStatus(idObject):
  doLog('ggggetStatus ' + str(idObject))
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      # probe for status
      success, data = make_get_request(f"{specs['hostname']}:{specs['port']}", '/engine/status')
      resData = json.loads(data)
      doLog(data)
      doLog(resData)
      doLog(resData['data']['details'])
      if success:
        return {
          'success': resData['status']['code'] == 200, 
          'online': resData['data']['engine_status'] == 'Running\n', 
          'enabled': True, 
          'data': json.dumps(resData['data']['details'])
        }
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    return {'success': False, 'data': str(e)}

def doStart(idObject):
  doLog('doStart ' + str(idObject))
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      success, data = make_get_request(f"{specs['hostname']}:{specs['port']}", '/engine/start')
      resData = json.loads(data)
      doLog(resData)
      if success:
        return {
          'success': resData['status']['code'] == 200, 
          'online': resData['data']['engine_status'] == 'Running\n', 
          'enabled': True, 
          'data': json.dumps(resData['data']['details'])
        }
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def doStop(idObject):
  doLog('doStop ' + str(idObject))
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      success, data = make_get_request(f"{specs['hostname']}:{specs['port']}", '/engine/stop')
      resData = json.loads(data)
      doLog(resData)
      if success:
        return {
          'success': resData['status']['code'] == 200, 
          'online': resData['data']['engine_status'] == 'Running\n', 
          'enabled': True, 
          'data': json.dumps(resData['data']['details'])
        }
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def ansStartBeats(idObject):
  doLog('ansStartBeats ' + str(idObject))
  ip = __getEngineIP(idObject)
  try: 
    if ip:
      data = startBeats(ip)
      doLog(data)
      return {'success': data['ok'], 'online': True, 'enabled': True, 'data': data}
      
    raise Exception( 'No specs' )
  except Exception as e:
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def ansStopBeats(idObject):
  doLog('ansStopBeats ' + str(idObject))
  ip = __getEngineIP(idObject)
  try: 
    if ip:
      data = stopBeats(ip)
      doLog(data)
      return {'success': data['ok'], 'online': False, 'enabled': True, 'data': data}
      
    raise Exception( 'No specs' )
  except Exception as e:
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def ansStartIPS(idObject):
  doLog('ansStartIPS ' + str(idObject))
  ip = __getEngineIP(idObject)
  try: 
    if ip:
      data = startIPS(ip)
      doLog(data)
      return {'success': data['ok'], 'online': True, 'enabled': True, 'data': data}
      
    raise Exception( 'No specs' )
  except Exception as e:
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def ansStopIPS(idObject):
  doLog('ansStopIPS ' + str(idObject))
  ip = __getEngineIP(idObject)
  try: 
    if ip:
      data = stopIPS(ip)
      doLog(data)
      return {'success': data['ok'], 'online': False, 'enabled': True, 'data': data}
      
    raise Exception( 'No specs' )
  except Exception as e:
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def ansStart(idObject):
  ip = __getEngineIP(idObject)
  try: 
    if ip:
      data = startBeats(ip)
      if not data['ok']:
        raise Exception('Failed to start beats - ' + str(data))
      data = startIPS(ip)
      return {'success': data['ok'], 'online': True, 'enabled': True, 'data': data}
  except Exception as e:
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def ansStop(idObject):
  ip = __getEngineIP(idObject)
  try: 
    if ip:
      data = stopBeats(ip)
      if not data['ok']:
        raise Exception('Failed to stop beats - ' + str(data))
      data = stopIPS(ip)
      return {'success': data['ok'], 'online': True, 'enabled': True, 'data': data}
  except Exception as e:
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def queryWebservers(idObject):
  doLog('queryWebservers ' + str(idObject))
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      success, data = make_get_request(f"{specs['hostname']}:{specs['port']}", '/engine/query/webservers')
      resData = json.loads(data)
      doLog(resData)
      if success:
        return {'success': resData['status']['code'] == 200, 'online': not resData['data']['status'], 'enabled': True, 'data': resData['data']}
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    traceback.print_exc()
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}
def queryModSecRules(idObject):
  doLog('queryModSecRules' + str(idObject))
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      success, data = make_post_request(f"{specs['hostname']}:{specs['port']}", '/engine/query/rules', {'idEnginetype': 2, 'webservers': ['apache2']})
      print("------------ data -----------");
      print(data)
      print(success)
      resData = json.loads(data)
      doLog(resData)
      if success:
        return {'success': resData['status']['code'] == 200, 'data': resData['data']}
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    traceback.print_exc()
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def queryRules(idObject, idEnginetype):
  doLog('queryRules' + str(idObject) + ' ' + str(idEnginetype))
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      success, data = make_post_request(f"{specs['hostname']}:{specs['port']}", '/engine/query/rules', {'idEnginetype': idEnginetype})
      print("------------ data -----------");
      print(data)
      print(success)
      resData = json.loads(data)
      doLog(resData)
      if success:
        return {'success': resData['status']['code'] == 200, 'data': resData['data']}
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    traceback.print_exc()
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}


def installRuleset(idObject, webserver, ruleset):
  doLog(f'Install ruleset: {webserver}, {ruleset}' )
  ip = __getEngineIP(idObject)
  try:
    if ip:
      data = installModSecRules(ip, webserver, ruleset)
      return {'success': data['ok'] and not data['failed'], 'online': False, 'enabled': True, 'data': data}
    else:
      raise BadRequest('no specs found')
  except Exception as e:
    return {'success': False, 'data': str(e)}
def uninstallRuleset(idObject, webserver, ruleset):
  doLog(f'Uninstall ruleset: {webserver}, {ruleset}' )
  ip = __getEngineIP(idObject)
  try:
    if ip:
      data = uninstallModSecRules(ip, webserver, ruleset)
      return {'success': data['ok'] and not data['failed'], 'online': False, 'enabled': True, 'data': data}
    else:
      raise BadRequest('no specs found')
  except Exception as e:
    return {'success': False, 'data': str(e)}

def getWatchList(idObject):
  doLog('getWatchList ' + str(idObject))
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      success, data = make_get_request(f"{specs['hostname']}:{specs['port']}", '/engine/watchList')
      print("------------ data -----------");
      resData = json.loads(data)
      if success:
        return {'success': resData['status']['code'] == 200, 'data': resData['data']}
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    traceback.print_exc()
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}

def updateWatchList(idObject, watchList):
  doLog('updateWatchList ' + str(idObject))
  specs = getEngineSpecs(idObject)
  try: 
    if specs:
      success, data = make_put_request(f"{specs['hostname']}:{specs['port']}", '/engine/watchList', watchList)
      print("------------ data -----------");
      resData = json.loads(data)
      if success:
        return {'success': resData['status']['code'] == 200, 'data': resData['data']}
      else:
        return {'success': False, 'data': data }
    return {'success': False, 'data': 'No specs'}
  except Exception as e:
    traceback.print_exc()
    doLog('EEEException' + str(e))
    return {'success': False, 'data': str(e)}
