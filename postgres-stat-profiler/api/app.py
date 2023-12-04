from flask import Flask, abort, jsonify, make_response, request, Response
from functools import wraps
from api_auth import api_auth
from api_keystore import api_keystore
import os
import datetime
import sys
import logging



logfilename = "log/pg-stat-profiler.log"

logging.basicConfig(filename = logfilename, level=logging.WARNING,
                    format='%(asctime)s[%(funcName)-5s] (%(processName)-10s) %(message)s',
                    )
logging.warning("Startup : Postgres Stat Profiler")
api_secret = os.getenv(u'PG_STAT_PROFILER_SECRET')
if api_secret:
      keystorefile = u'log/pg-stat-profiler-keystore'
      keystore = api_keystore(api_secret,keystorefile)
else:
      logging.warning("Exception Shutdown : Postgres Stat Profiler: No secret supplied")


app = Flask(__name__)

def fail_authenticate():
    return make_response(jsonify({'error': 'Not Authenticated'}), 401)

def requires_secret_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request_auth = api_auth(request)
        if not request_auth.getValid():
            return fail_authenticate()  
        else:
            requestkey = str(request_auth.getRequestkey()).lower().strip()
            if not api_secret == requestkey:
                return fail_authenticate()
        return f(*args, **kwargs)
    return decorated

def requires_api_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request_auth = api_auth(request)
        if not request_auth.getValid():
            return fail_authenticate()  
        else:
            requestkey = str(request_auth.getRequestkey()).lower().strip()
            if not keystore.checkKey(requestkey):
                return fail_authenticate()
        return f(*args, **kwargs)
    return decorated


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(503)
def not_supported(error):
    return make_response(jsonify({'error': 'Not Supported'}), 503)

@app.route('/_api/v1.0')
@requires_secret_auth
def publish_welcome():
   try: 
    return jsonify({'postgres-stat-profiler':'welcome','version': '1.0.0'}) 
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/v1.0/getApikeys')
@requires_secret_auth
def show_apikeys():
   try: 
    keys = []
    for i in range(0,5):
        keys.append(keystore.getApiKey(i))
    return make_response(jsonify({'apikeys': '{}'.format(str(keys))}),200)
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 


if __name__ == '__main__':
 try:
      app.debug = True
      app.run()
 except Exception as e:
  logging.warning("Exception Shutdown : Postgres Stat Profiler: Error ["+str(e)+"]")

# Helper functions

