from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from ..portability import quote
from ..elasticsearch_utils import delete_index
from werkzeug.exceptions import *
from flask import session,request,after_this_request
from ..config_utils import config

import json
__db = DbInstance.getInstance()

dialect = config.get('Default', 'dialect', fallback="")

class Object(__db.Base):
  __tablename__ = "object"
  idObject = Column(Integer, primary_key = True)
  name = Column(String(50))
  idEngine = Column(Integer, ForeignKey('engine.idEngine', ondelete='CASCADE'))
  description = Column(String(255))



  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idObject" in dictModel) and (dictModel["idObject"] != None):
      self.idObject = dictModel["idObject"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("idEngine" in dictModel) and (dictModel["idEngine"] != None):
      self.idEngine = dictModel["idEngine"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

  def __repr__(self):
    return '<Object idObject={} name={} idEngine={} description={} >'.format(self.idObject, self.name, self.idEngine, self.description, )

  def json(self):
    return {
      "idObject":self.idObject,"name":self.name,"idEngine":self.idEngine,"description":self.description,
    }

  def update(self, dictModel):
    if ("idObject" in dictModel) and (dictModel["idObject"] != None):
      self.idObject = dictModel["idObject"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("idEngine" in dictModel) and (dictModel["idEngine"] != None):
      self.idEngine = dictModel["idEngine"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

def __getEngineSpecs(idEngine):
  sql = 'SELECT #specs# from engine where #idEngine#=:idEngine'
  sql = quote(sql, dialect)
  results = __db.session().execute(sql, {'idEngine': idEngine}).fetchall()
  return json.loads(results[0][0])
def __get_ip_from_specs(specs):
  return specs['hostname']

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Object).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Object).filter(Object.idObject == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doGetDetails(id):
  sql = """
SELECT 
  o.#idObject#, o.#idEngine#, o.description, o.name, et.#idEnginetype#
FROM #object# o
  LEFT JOIN engine e
    ON o.#idEngine# = e.#idEngine#
  LEFT JOIN enginetype et
    on e.#idEnginetype# = et.#idEnginetype#
WHERE
  o.#idObject# = :idObject
  """
  sql = quote(sql, dialect)
  results = __db.session().execute(sql, {'idObject': id}).fetchall()
  if len(results) == 0 :
    raise BadRequest('Not found');
  result = results[0];
  return {'idObject': result[0], 'idEngine': result[1], 'description': result[2], 'name': result[3], 'idEnginetype': result[4]}

def __doUpdate(id, model):
  instance = getObject(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance

def __stopNode(specs):
  try: 
    doLog('__stopNode', True);
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

def __doDelete(id):
  instance = getObject(id)

  if instance.idEngine is not None:
    specs = __getEngineSpecs(instance.idEngine)
    resData = __stopNode(specs)
    print(resData)
    if not resData['success']:
      raise BadRequest('Cannot stop hostIPS node')

    ip = __get_ip_from_specs(specs)
    success, data = delete_index(f'metricbeat-7.11-{ip}-*')
    print(success, data)
    if not success:
      raise BadRequest('Cannot remove historic data of node')
    
    try:
      sql = '''DELETE
        FROM #rulepackageObjectRel# rpor
        WHERE rpor.#idObject# = :idObject
      '''
      sql = quote(sql, dialect)
      __db.session().execute(sql, {'idObject': id})
      __db.session().commit()
    except Exception as e:
      __db.session().rollback()
      raise BadRequest(str(e))

  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Object).filter_by(**model).all()
  __db.session().commit()
  return results


def listObjects():
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

def newObject(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Object(model)
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

def getObject(id):
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

def getObjectDetails(id):
  try:
    return __doGetDetails(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGetDetails(id)
  except InterfaceError as e:
    doLog(e)
    __recover()
    return __doGetDetails(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e


def updateObject(id, model):
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

def deleteObject(id):
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

def findObject(model):
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

def __doListIPSObjects():
  sql = '''SELECT
      o.#idObject#, o.name, o.description, e.specs, e.#idEnginetype#
    FROM object o 
      INNER JOIN engine as e ON o.#idEngine# = e.#idEngine#
  '''
  sql = quote(sql, dialect)
  results = __db.session().execute(sql, {}).fetchall()
  return list(map(lambda x: {'idObject':x[0], 'name':x[1], 'description': x[2], 'specs': x[3], 'idEnginetype': x[4]}, results))

def listIPSObjects():
  doLog("List all IPS objects")
  try:
    return __doListIPSObjects()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doListIPSObjects()
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e
