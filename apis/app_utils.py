from hashlib import sha256
from flask import jsonify
from jwt import encode, decode
from apis import config
import time
from functools import wraps

print(config)
SALT = 'uet-ips-man'
JWT_SETCRET = config.get('Default', 'JWT_SECRET', fallback='thisissecret')

def doHash(str):
  str1 = SALT + str
  hashObj = sha256(str1.encode('UTF-8'))
  return hashObj.hexdigest()
def doGenJWT(obj, salt=JWT_SETCRET):
  obj['iat'] = int(time.time())
  obj['exp'] = int(config.get('Default', 'JWT_EXP', fallback=86400)) + int(time.time())
  return encode(obj, salt).decode('utf-8')
def doParseJWT(key, salt=JWT_SETCRET):
  try:
    return decode(key, salt)
  except: 
    return None
def doLog(message, error = False):
  if error:
    print("*** %s" % message)
  else:
    print("--- %s" % message)
def doClear(dict):
  keys = [ k for k in dict ]
  for key in keys:
    del dict[key]
def matchOneOf(request, prefixes):
  for prefix in prefixes:
    if request.path.startswith(prefix[0]) and (prefix[1] is None or request.method == prefix[1]):
      return True
  return False

def require_permission(permission: str):
  def inner(f):
    @wraps(f)
    def decorated(*args, **kwargs):
      return f(*args, **kwargs)
    return decorated
  return inner