
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