from .db_utils import DbInstance
from .app_utils import doLog
from sqlalchemy.exc import *

from .objects import Object
from .engines import Engine
import json

__db = DbInstance.getInstance()

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
    __db.newSession()
    return getEngineSpecs(idObject)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e
