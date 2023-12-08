import base64 
import os
import logging

class connection:

    def __init__(self,data):
        self.valid = False
        if 'host' in data and \
        'port' in data and \
        'cacert' in data and \
        'credentials' in data and \
        'database' in data:
            self.host = data['host']
            self.port = data['port']
            self.cacert = data['cacert']
            self.credentials = data['credentials']
            self.database = data['database']
            self._setUsernamePassword()
            self.valid = True

    def getValid(self):
        return self.valid
    
    def getAllDetails(self):
        try: 
          details = u"'database' : '{}', 'host': '{}', 'port' : {}, 'cacert' : '{}', 'credentials' : '{}'".format\
            (self.database,self.host,self.port,self.cacert,self.credentials)
          return details
        except:
          return u'{ "error" : "connection details missing" }'
    
    def getApiDetails(self):
        try: 
          details = u"'database' : '{}', 'host': '{}', 'port' : {}, 'cacert' : '{}'".format(self.database,self.host,self.port,self.cacert)
          return details
        except:
          return u'{ "error" : "connection details missing" }'
        
    def getConnectionString(self):
     try:
         sslrootcert = os.path.join(os.getenv(u'PG_STAT_PROFILER_BASE'),u'resources/cert/{}'.format(self.cacert))
         return ' dbname = {} host = {} port = {} user = {} password = {} sslmode = require sslrootcert = {}'.\
            format(self.database,self.host,self.port,self.username,self.password, sslrootcert)
     except Exception as e:
         logging.warning('pg-stat-profiler : unexpected profile-getConnectionString error : [{}]'.format(str(e)))
        

    def update(self,data):
       if 'database' in data:
          self.database = data['database']
       if 'host' in data:
          self.host = data['host']
       if 'port' in data:
          self.port = data['port']
       if 'cacert' in data:
          self.cacert = data['cacert']
       if 'credentials' in data:
          self.credentials = data['credentials']
          self._setUsernamePassword()

    def _setUsernamePassword(self):
          src_credbytes = base64.urlsafe_b64decode(self.credentials)          
          src_credparts = src_credbytes.decode(u'utf-8').split(':')
          if len(src_credparts) == 2:
                self.username = src_credparts[0]
                self.password = src_credparts[1]

    def __str__(self):
        return str(self.__dict__)
        