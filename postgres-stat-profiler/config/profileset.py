import os
import base64
import json
import logging
from cryptography.fernet import Fernet
from config.profile import profile

class profileset:

    def __init__(self,secret,profilesfilename):
        self.profiles = {}
        self.valid = True
        secret_bytes = secret.encode(u"utf-8")
        fernetkey = base64.urlsafe_b64encode(secret_bytes.ljust(32)[:32])
        self.fernet = Fernet(fernetkey)
        self.profilesfilename = profilesfilename
        if os.path.isfile(self.profilesfilename):
           self.valid = self._fetchProfiles()

    def hasName(self,name):
        if name in self.profiles:
            return True
        return False
    
    def _getAllDetails(self,name):
        if name in self.profiles:
            return self.profiles[name].getAllDetails()
        else:
            return '"error" : Not found"'
        
    def getApiDetails(self,name):
        if name in self.profiles:
            return self.profiles[name].getApiDetails()
        else:
            return '"error" : Not found"'
        
    def addProfileApi(self,name,request):
        status = False
        try:
           if name not in self.profiles:
              if request.headers.get('Content-Type'):
                  data = request.get_json()
                  data['name'] = name
                  status = self.addProfile(name,data)
           return status
        except Exception as e:
           logging.warn('pg-stat-profiler : unexpected profile-apiadd error : [{}]'.format(str(e)))
           return False
        
    def addProfile(self,name,data):
        status = False
        try:
            self.profiles[name] = profile(data)
            if name in self.profiles and self.profiles[name].getValid():
                     status = self._updateProfilesFile()
            return status
        except Exception as e:
            logging.warn('pg-stat-profiler : unexpected profile-add error : [{}]'.format(str(e)))
            return False
        
    def _updateProfilesFile(self):
       status = False
       try: 
          cf = open(self.profilesfilename,'w')
          for profile in self.profiles:
             result = json.dumps(self.profiles[profile].getAllDetails())
             profilestring = json.dumps(result)
             encryptedstring = self.fernet.encrypt(profilestring.encode('utf-8'))
             cf.write(encryptedstring.decode('utf-8') + '\n')
          cf.close()
          status = True
       except:
          status = False
       return status

    def _fetchProfiles(self):
       status = False
       cf = open(self.profilesfilename,'r')
       cflines = cf.readlines()
       for cfline in cflines:
          try:
             result = self.fernet.decrypt(cfline.encode(u"utf-8")).decode("utf-8")
             if result:
                try:
                   # required to remove \\ characters popped by the fernet url encryot-decrypt process
                   thisprofile = json.loads(json.loads(json.loads(result)))
                   if thisprofile and 'name' in thisprofile:
                       status = self.addProfile(thisprofile['name'],thisprofile)
                except Exception as e:
                  logging.warn('pg-stat-profiler : unexpected profile-fetch error : [{}]'.format(str(e)))
                  status = False
                  break
          except Exception as e:
             logging.warn('pg-stat-profiler : unexpected profile-fetch error : [{}]'.format(str(e)))
             status = False
             break
       return status




    