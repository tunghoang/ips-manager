from flask import Flask, session, request
from apis import api
from apis.db_utils import DbInstance
from apis.app_utils import *
from flask_session import Session
from werkzeug.exceptions import *
from werkzeug.contrib.fixers import ProxyFix
import os
from flask import g


db = DbInstance.getInstance()

app = Flask("ips-manager")
app.wsgi_app = ProxyFix(app.wsgi_app)
server_name = os.getenv("SERVER_NAME","localhost:8000")
print(server_name)
app.config['SERVER_NAME'] = server_name
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/ipsman'
app.config['MAX_CONTENT_LENGTH'] = 750 * 1024 * 1024
app.secret_key = os.urandom(16)
api.init_app(app)

Session(app)

@app.before_request
def before_request():
  key = request.cookies.get('key')
  jwt = request.cookies.get('jwt')
  key = key if key is not None else request.headers.get('auth-key')
  jwt = jwt if jwt is not None else request.headers.get('authorization')

  no_auth_routes = ( '/', '/favicon.ico', '/swagger.json', '/bot_alert/' )
  no_auth_prefixes = ( '/swaggerui', '/login', '/control', '/rulepackages' )
  #no_auth_prefixes = ( '/' )

  if request.path in no_auth_routes or matchOneOf(request.path, no_auth_prefixes) :
    return None
  elif jwt is None or key is None:
    doLog("Invalid request")
    raise Unauthorized("Invalid request")
  elif key in session:
    doLog('Check session')
    salt = session[key]
    try:
      decoded = doParseJWT(jwt, salt)
      if not decoded:
        raise Unauthorized("Invalid token")
      g.username = decoded['username']
      g.idUser = decoded['idUser']

    except:
      raise Unauthorized("Invalid session")
  else:
    raise Unauthorized("Not login")

db.Base.metadata.create_all(db.engine)

if __name__ == "__main__":
  app.run()
