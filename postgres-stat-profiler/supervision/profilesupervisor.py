import logging
import time
import os
import multiprocessing
from config.profilestore import profilestore

class profilesupervisor():

    def __init__(self,api_secret,profilesfile):
        self.profilesfile = profilesfile
        self.api_secret = api_secret
        self.profilejobs = {}
        self.profilestore = profilestore(self.api_secret,self.profilesfile)

    def getProfilestore(self):
        return self.profilestore

    def run(self):
        try:
         while True:
            # refresh profiles from file (persistent store) each cycle
            self.profilestore = profilestore(self.api_secret,self.profilesfile)
            # use list() to avoid runtime error when deleting a object property during iteration
            for pname,p in list(self.profilestore.getProfiles().items()):
                #logging.warning('pg-stat-profiler : Reviewing profile execution : [{}] [{}]'.format(pname,p.getStatus()))
                # stop existing process if disabled via api
                if pname in self.profilejobs and p.getStatus() == 'disabled':
                    logging.warning('pg-stat-profiler : Disabling profile execution : [{}]'.format(pname))
                    self.profilejobs[pname].terminate()
                    self.profilejobs[pname].join()
                    del self.profilejobs[pname]
                    logging.warning('pg-stat-profiler : Disable profile execution success : [{}]'.format(pname))
                # start process if new or enabled via api
                if pname not in self.profilejobs and p.getStatus() == 'enabled':
                    logging.warning('pg-stat-profiler : Enabling profile execution : [{}]'.format(pname))
                    thisprocess = multiprocessing.Process(target=p.run,args=())
                    self.profilejobs[pname] = thisprocess
                    self.profilejobs[pname].start()
                    logging.warning('pg-stat-profiler : Enable profile execution success : [{}]'.format(pname))
            for jname in list(self.profilejobs.keys()):
                # stop existing process if deleted via api
                #logging.warning('pg-stat-profiler : Reviewing profile execution : [{}]'.format(jname))
                if jname not in self.profilestore.getProfiles():
                    logging.warning('pg-stat-profiler : Disabling profile execution : [{}]'.format(jname))
                    self.profilejobs[jname].terminate()
                    self.profilejobs[jname].join()
                    del self.profilejobs[jname]
                    logging.warning('pg-stat-profiler : Disable profile execution success : [{}]'.format(jname))
            time.sleep(10)
        except Exception as e:
            logging.warning('pg-stat-profiler : profilesupervisor unexpected error : [{}]'.format(str(e)))


         
