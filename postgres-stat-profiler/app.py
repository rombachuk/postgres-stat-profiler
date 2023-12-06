import sys
import os
import logging
import json
from flask import Flask, abort, jsonify, make_response, request, Response
from copy import deepcopy
from functools import wraps
from api.api_auth import api_auth
from api.api_keystore import api_keystore
from config.profilestore import profilestore

os.environ['PG_STAT_PROFILER_SECRET'] = '4958034759875304895734897543875403985740987540785078438859074'
os.environ['PG_STAT_PROFILER_BASE'] = '/Users/y7kwh/Documents/GitHub/postgres-stat-profiler/postgres-stat-profiler'
logfilename = os.path.join(os.getenv(u'PG_STAT_PROFILER_BASE'),u"resources/log/pg-stat-profiler.log")
keystorefile = os.path.join(os.getenv(u'PG_STAT_PROFILER_BASE'),u'resources/sec/pg-stat-profiler.keystr')
profilesfile = os.path.join(os.getenv(u'PG_STAT_PROFILER_BASE'),u'resources/sec/pg-stat-profiler.prof')

logging.basicConfig(filename = logfilename, level=logging.WARNING,
                    format='%(asctime)s[%(funcName)-5s] (%(processName)-10s) %(message)s',
                    )
logging.warning("Startup : Postgres Stat Profiler")

api_secret = os.getenv(u'PG_STAT_PROFILER_SECRET')
if api_secret:  
      keystore = api_keystore(api_secret,keystorefile)
      profilestore = profilestore(api_secret,profilesfile)
else:
      logging.warning("Exception Shutdown : Postgres Stat Profiler: No secret supplied")
      sys.exit()


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
@requires_api_auth
def publish_welcome():
   try: 
    return jsonify({'postgres-stat-profiler':'welcome','version': '1.0.0'}) 
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/v1.0/apikeys')
@requires_secret_auth
def show_apikeys():
   try: 
    keys = []
    for i in range(0,5):
        keys.append(keystore.getApiKey(i))
    return make_response(jsonify({'apikeys': '{}'.format(str(keys))}),200)
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 
   
@app.route('/_api/v1.0/profiles',methods=['GET'])
@requires_api_auth
def read_profiles():
   try: 
       if len(profilestore.getProfiles()) > 0:
          details = []
          for p in profilestore.getProfiles():
            details.append(profilestore.getApiDetails(p))
          return jsonify(details,200)
       else:
         return make_response(jsonify({'error': 'Not Found'}), 404)
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/v1.0/profiles/<name>',methods=['GET'])
@requires_api_auth
def read_profile(name):
   try: 
    if profilestore.hasName(name):
       result = profilestore.getApiDetails(name)
       if 'name' in result:
          return jsonify(profilestore.getApiDetails(name),200)
    return make_response(jsonify({'error': 'Not Found'}), 404)
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/v1.0/profiles/<name>',methods=['POST'])
@requires_api_auth
def create_profile(name):
   try:
    if profilestore.addProfileApi(name,request):
        return jsonify({'result':'ok'},200) 
    else:
        return jsonify({'result':'error'},200) 
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/v1.0/profiles/<name>',methods=['PUT'])
@requires_api_auth
def update_profile(name):
   try: 
    if profilestore.updateProfileApi(name,request):
        return jsonify({'result':'ok'},200) 
    else:
        return jsonify({'result':'error'},200) 
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/v1.0/profiles/<name>',methods=['DELETE'])
@requires_api_auth
def delete_profile(name):
   try: 
    if profilestore.deleteProfileApi(name):
        return jsonify({'result':'ok'},200) 
    else:
        return jsonify({'result':'error'},200) 
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

if __name__ == '__main__':
 try:
      app.debug = False
      app.run(ssl_context='adhoc')
 except Exception as e:
  logging.warning("Exception Shutdown : Postgres Stat Profiler: Error ["+str(e)+"]")
  sys.exit()

# Helper functions

