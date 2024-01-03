import uuid
import base64
import os
from cryptography.fernet import Fernet

class api_keystore:

    def __init__(self,secret,keyfilename):
        self.apikeys = []
        self.keyfilename = keyfilename
        secret_bytes = secret.encode(u'utf-8')
        fernetkey = base64.urlsafe_b64encode(secret_bytes.ljust(32)[:32])
        self.fernet = Fernet(fernetkey)
        if not os.path.isfile(self.keyfilename) or not self.checkKeyfile():  
           self.resetKeys()

    def checkKeyfile(self):
       status = False
       self.apikeys = []
       cf = open(self.keyfilename,'r')
       cflines = cf.readlines()
       for cfline in cflines:
          try:
             result = self.fernet.decrypt(cfline.encode(u'utf-8')).decode(u'utf-8') 
          except:
             result = False
          if result:
             thiskey = self.fernet.encrypt(result.encode(u'utf-8'))
             self.apikeys.append(thiskey)
             status = True
          else:
             status = False
             break
       cf.close()
       return status


    def getApiKey(self,index):
        try:
          result = self.fernet.decrypt(self.apikeys[index]).decode("utf-8")
        except:
          result = u'error'
        return result
    
    def resetKeys(self):
         self.apikeys = []
         keyfile = open(self.keyfilename,'w')
         for i in range(0, 5):
           apikey = '{}{}'.format(uuid.uuid4().hex,uuid.uuid4().hex)
           thiskey = self.fernet.encrypt(apikey.encode('utf-8'))
           self.apikeys.append(thiskey)
           keyfile.write(thiskey.decode('utf-8') + '\n')
         keyfile.close()

    def checkKey(self,testKeyString):
       cf = open(self.keyfilename,'r')
       cflines = cf.readlines()
       for cfline in cflines:
          result = self.fernet.decrypt(cfline.encode(u"utf-8")).decode("utf-8") 
          if result == testKeyString:
             cf.close()
             return True
       cf.close()
       return False
    
    def __str__(self):
        return str(self.__dict__)
 
            
           