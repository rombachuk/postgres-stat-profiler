import base64 
import os
import logging

class connection:

    def __init__(self,data):
        self.valid = False
        try:
           if 'type' in data and \
           'host' in data and \
           'port' in data and \
           'credentials' in data and \
           'database' in data:
               self.type = data['type']
               self.host = data['host']
               self.port = data['port']                 
               self.credentials = data['credentials']
               self.database = data['database']
               self._setUsernamePassword()
           if 'sslmode' in data:
               self.sslmode = data['sslmode'] 
               if 'cacert' in data:
                   # allow for environment variables in the cacert location
                   self.cacert = os.path.expandvars(data['cacert'])
                   if os.path.isfile(self.cacert):
                       self.valid = True 
                   else:
                       logging.warning(u'pg-stat-profiler : Missing cacert file')
                       self.valid = False
               else:
                   self.cacert = 'notsupplied'
                   if self.sslmode == 'verify-ca' or self.sslmode == 'verify-full':
                       self.valid = False
                       logging.warning(u'pg-stat-profiler : No cacert provided for verify connection')
                   else:
                       self.valid = True               
           else:
               self.sslmode = 'require'
               self.cacert = 'notapplicable'
               self.valid = True
        except:
               self.valid = False

    def getValid(self):
        return self.valid
    
    def getType(self):
        return self.type
    
    def getAllDetails(self):
        try: 
          details = u'"database": "{}", "type": "{}", "host": "{}", "port": {}, "cacert": "{}", "sslmode": "{}", "credentials": "{}"'.format\
            (self.database,self.type,self.host,self.port,self.cacert,self.sslmode,self.credentials)
          return details
        except:
          return u'{ "error" : "connection details missing" }'
    
    def getApiDetails(self):
        try: 
          details = u'"database": "{}",  "type": "{}", "host": "{}", "port": {}, "cacert": "{}", "sslmode": "{}"'.format\
            (self.database,self.type,self.host,self.port,self.cacert, self.sslmode)
          return details
        except:
          return u'{ "error" : "connection details missing" }'
        
    def getPostgresConnectionString(self):
     try:
         if self.type == u'postgresql':
            return ' dbname = {} host = {} port = {} user = {} password = {} sslmode = {} sslrootcert = {}'.\
            format(self.database,self.host,self.port,self.username,self.password, self.sslmode, self.cacert)
         else:
            return ''
     except Exception as e:
         logging.warning('pg-stat-profiler : unexpected profile-getPostgresConnectionString error : [{}]'.format(str(e)))
         return u'{ "error" : "postgres connection string configuration issue" }'
        

    def update(self,data):
       if 'database' in data:
          self.database = data['database']
       if 'type' in data:
          self.type = data['type']
       if 'host' in data:
          self.host = data['host']
       if 'port' in data:
          self.port = data['port']
       if 'sslmode' in data:
          self.cacert = data['sslmode']
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
        