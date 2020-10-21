from flask import Flask, session, request
from apis import api
from apis.db_utils import DbInstance
from apis.app_utils import *
from werkzeug.exceptions import *
from werkzeug.contrib.fixers import ProxyFix
import os
from flask import g


db = DbInstance.getInstance()

app = Flask("ips-manager")
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['SERVER_NAME'] = "localhost:8000"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp'
app.secret_key = os.urandom(16)
api.init_app(app)


@app.before_request
def before_request():
  key = request.cookies.get('key')
  jwt = request.cookies.get('jwt')
  key = key if key is not None else request.headers.get('auth-key')
  jwt = jwt if jwt is not None else request.headers.get('authorization')

  no_auth_routes = ( '/', '/favicon.ico', '/swagger.json' )
  no_auth_prefixes = ( '/swaggerui', '/login' )

  if request.path in no_auth_routes or matchOneOf(request.path, no_auth_prefixes) :
    return None

  if key is None or jwt is None:
    raise Unauthorized("Invalid request")

  if key not in session:
    raise Unauthorized("You are not login")

  decoded = doParseJWT(jwt, session[key])

  g.username = decoded['username']

  return None

db.Base.metadata.create_all(db.engine)

if __name__ == "__main__":
  app.run()
