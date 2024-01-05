import sys
import os
import logging
from flask import Flask, abort, jsonify, make_response, request, Response
from flask_apscheduler import APScheduler
from functools import wraps
import multiprocessing
from postgres_stat_profiler.api_auth.api_auth import api_auth
from postgres_stat_profiler.api_auth.api_keystore import api_keystore
from postgres_stat_profiler.config.profilestore import profilestore
from postgres_stat_profiler.supervision.profilesupervisor import profilesupervisor

# environment

installbase = os.path.expandvars(os.getenv(u'PG_STAT_PROFILER_BASE'))
if not installbase:
   print('pg-stat-profiler: Failed to find environment variable PG_STAT_PROFILER_BASE, using cwd')
   installbase = os.getcwd()
secbase = os.path.join(installbase,u'postgres_stat_profiler/resources/sec')
if not os.path.isdir(secbase):
   print('pg-stat-profiler: Failed to find security directory, exiting...')
   print('pg-stat-profiler: Check [Invalid Install base={}]'.format(str(installbase)))
   print('pg-stat-profiler: Please supply correct environment variable PG_STAT_PROFILER_BASE'.format(str(installbase)))
   sys.exit()

logbase = os.path.expandvars(os.getenv(u'PG_STAT_PROFILER_LOGBASE'))
if not logbase:
   print('pg-stat-profiler: Failed to find environment variable PG_STAT_PROFILER_LOGBASE, using cwd')
   logbase = os.getcwd()
if not os.path.isdir(logbase):
   print('pg-stat-profiler: Failed to initiate logging, exiting...')
   print('pg-stat-profiler: Reason [Invalid Environment Variable PG_STAT_PROFILER_LOGBASE={}]'.format(str(logbase)))
   sys.exit()

api_secret = os.getenv(u'PG_STAT_PROFILER_SECRET')
if not api_secret:  
      print("pg-stat-profiler: Failed to find secret, exiting...")
      print("Failed to find environment variable PG_STAT_PROFILER_SECRET")
      sys.exit()

# profile supervisor control function: runs periodically in parallel with Flask

def check_supervisorjob():
  global supervisorjob
  global profilesqueue
  global profile_supervisor
  global profile_store
  try:
   # 
   if not supervisorjob.is_alive():
      supervisorjob.join()
      supervisorjob = multiprocessing.Process(target=profile_supervisor.run,args=(profilesqueue,))
      supervisorjob.start()
      logging.warning("pg-stat-profiler: supervisor restarted with processid :[{}]".format(str(supervisorjob.pid)))
   else:
     #  handle profile state changes passed from individual profiles up via supervisor
     #  ensures that only this main thread updates the persistent profilesfilestore
     while not profilesqueue.empty(): 
        qdata = profilesqueue.get()
        if 'name' in qdata:
           profile_store.updateProfile(qdata['name'],qdata)
  except Exception as e:
      logging.warning("pg-stat-profiler: Error checking supervisor :[{}]".format(str(e)))

# main api Flask section

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

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
       if len(profile_store.getProfiles()) > 0:
          details = []
          for p in profile_store.getProfiles():
            details.append(profile_store.getApiDetails(p))
          return jsonify(details,200)
       else:
         return make_response(jsonify({'error': 'Not Found'}), 404)
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/v1.0/profiles/<name>',methods=['GET'])
@requires_api_auth
def read_profile(name):
   try: 
    if profile_store.hasName(name):
       result = profile_store.getApiDetails(name)
       if 'name' in result:
          return jsonify(result,200)
    return make_response(jsonify({'error': 'Not Found'}), 404)
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/v1.0/profiles/<name>',methods=['POST'])
@requires_api_auth
def create_profile(name):
   try:
    if profile_store.addProfileApi(name,request):
        return jsonify({'result':'ok'},200) 
    else:
        return jsonify({'result':'error'},200) 
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/v1.0/profiles/<name>',methods=['PUT'])
@requires_api_auth
def update_profile(name):
   try: 
    if profile_store.updateProfileApi(name,request):
        return jsonify({'result':'ok'},200) 
    else:
        return jsonify({'result':'error'},200) 
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/v1.0/profiles/<name>',methods=['DELETE'])
@requires_api_auth
def delete_profile(name):
   try: 
    if profile_store.deleteProfileApi(name):
        return jsonify({'result':'ok'},200) 
    else:
        return jsonify({'result':'error'},200) 
   except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

def main():
  global supervisorjob
  global profilesqueue
  global keystore
  global profile_store
  global profile_supervisor
  try:
      logfilename = os.path.join(logbase,u"pg-stat-profiler.log")
      logging.basicConfig(filename = logfilename, level=logging.WARNING,
                    format='%(asctime)s[%(funcName)-5s] (%(processName)-10s) %(message)s',
                    )
      try:
         logging.warning("Startup : postgres-stat-profiler : process logging")
      except Exception as e:
         print('pg-stat-profiler: Failed to initiate logging, exiting... Reason [{}]'.format(str(e)))
         sys.exit()

      try: 
         keystorefile = os.path.join(secbase,u'.pg-stat-profiler.keystr')
         profilesfile = os.path.join(secbase,u'.pg-stat-profiler.prof')
         keystore = api_keystore(api_secret,keystorefile)
         profile_store = profilestore(api_secret,profilesfile)
         profile_supervisor = profilesupervisor(api_secret,profilesfile)
      except Exception as e:
         print('pg-stat-profiler: Failed to initiate data with secret, exiting... Reason [{}]'.format(str(e)))
         sys.exit()
      
      profilesqueue = multiprocessing.Queue()
      supervisorjob = multiprocessing.Process(target=profile_supervisor.run, args=(profilesqueue,))
      supervisorjob.start()
      scheduler.add_job(id=u'periodic_supervisorcheck',func=check_supervisorjob, trigger='interval', seconds=10)      
      app.debug = False
      app.run(ssl_context='adhoc')
  except Exception as e:
      logging.warning("Exception Shutdown : postgres-stat-profiler: Error ["+str(e)+"]")
      sys.exit()

if __name__ == '__main__':
   main()

# Helper functions

