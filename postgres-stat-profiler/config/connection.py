import base64 

class connection:

    def __init__(self,data):
        self.valid = False
        if 'host' in data and \
        'port' in data and \
        'cacert' in data and \
        'credentials' in data:
            self.host = data['host']
            self.port = data['port']
            self.cacert = data['cacert']
            self.credentials = data['credentials']
            self._setUsernamePassword()
            self.valid = True

    def getValid(self):
        return self.valid
    
    def getAllDetails(self):
        try: 
          details = u'"host": "{}", "port" : {}, "cacert" : "{}", "credentials" : "{}"'.format\
            (self.host,self.port,self.cacert,self.credentials)
          return details
        except:
          return u'{ "error" : "connection details missing" }'
    
    def getApiDetails(self):
        try: 
          details = u"'host': '{}', 'port' : {}, 'cacert': '{}'".format(self.host,self.port,self.cacert)
          return details
        except:
          return u'{ "error" : "connection details missing" }'
        
    def update(self,data):
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
        