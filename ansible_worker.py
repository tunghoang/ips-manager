import traceback
from apis.db_utils import DbInstance
from apis.config_utils import config
from apis.portability import quote
import time
from datetime import datetime
import logging
import logging.config
import json
from apis.ansible_utils import *
logging.config.fileConfig(fname='ansible_worker.ini')

logger = logging.getLogger('WORKER_LOGGER')

dialect = config.get('Default', 'dialect', fallback = '')

__db = DbInstance.getInstance()

def updateRulepackageObjectRel(session, idRulepackageobjectrel, synced = True, errored = False):
  try:
    sql = 'UPDATE #rulepackageObjectRel# SET synced = :synced, errored = :errored WHERE #idRulepackageobjectrel# = :idRulepackageobjectrel'
    sql = quote(sql, dialect)
    session.execute(sql, {'synced': synced, 'errored': errored, 'idRulepackageobjectrel': idRulepackageobjectrel})
    session.commit()
  except Exception as e:
    traceback.print_exc()
    session.rollback()

sql_stm = '''
SELECT 
  obj.#idObject#, obj.name, en.specs, entype.#idEnginetype#, entype.name, rp.application, rp.version, rporel.#idRulepackageobjectrel#
FROM object obj 
  INNER JOIN engine en
    ON obj.#idEngine# = en.#idEngine#
  INNER JOIN enginetype entype
    ON en.#idEnginetype# = entype.#idEnginetype#
  INNER JOIN #rulepackageObjectRel# rporel
    ON obj.#idObject# = rporel.#idObject#
  INNER JOIN rulepackage rp
    ON rporel.#idRulepackage# = rp.#idRulepackage#
WHERE rporel.synced is NOT TRUE AND rporel.errored is NOT TRUE AND rp.#idEnginetype# = en.#idEnginetype#
'''
sql_stm = quote(sql_stm, dialect)
while True:
  try:
    __db.newSession()
    logger.info('spawn new sesssion to db');
    results = __db.session().execute(sql_stm, {}).fetchall();
    if len(results) > 0:
      for r in results:
        logger.info("update rulepackage to : node=%s application=%s version=%s", r[1], r[5], r[6])
        specs = json.loads(r[2])
        ip = specs['hostname']
        application = r[5]
        version = r[6]
        try:
          ret = installApplicationRules(ip, application, version)
          print(f'RESULT -- {str(ret)}')
          if ret['ok'] and not ret['failed']:
            updateRulepackageObjectRel(__db.session(), r[7], True, False)
          else:
            updateRulepackageObjectRel(__db.session(), r[7], False, True)
        except Exception as e:
          raise e
  except Exception as e:
    logger.error(str(e))
    __db.session().rollback()
  time.sleep(30)
