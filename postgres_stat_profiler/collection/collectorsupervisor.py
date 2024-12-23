import logging
import logging.handlers
import time
import multiprocessing
from postgres_stat_profiler.config.profilestore import profilestore
from postgres_stat_profiler.collection.collector import collector

class collectorsupervisor():

    def __init__(self,api_secret,profilesfile):
        self.profilesfile = profilesfile
        self.api_secret = api_secret
        self.profilestore = profilestore(self.api_secret,self.profilesfile) 
        self.collectorjobs = {}
        
       
    def getProfilestore(self):
        return self.profilestore

    def run(self, profilesqueue, loggingqueue):
        try:
         h = logging.handlers.QueueHandler(loggingqueue) 
         logger = logging.getLogger()
         logger.addHandler(h)
         logging.warn('pg_stat_profiler: profilesupervisor started')

         while True:
            # refresh profiles from file (persistent store) each cycle
            # 
            self.profilestore = profilestore(self.api_secret,self.profilesfile)
            # 
            # check jobs against the profile status set by api, and also if jobs have crashed
            # use list() to avoid runtime error when deleting a object property during iteration
            for pname,profile in list(self.profilestore.getProfiles().items()):
                #logging.warning('pg-stat-profiler : Reviewing profile collection : [{}] [{}]'.format(pname,p.getStatus()))
                # stop existing collector process if disabled via api
                if pname in self.collectorjobs and profile.getStatus() == 'disabled':
                    logging.warning('pg-stat-profiler : Disabling profile collection : [{}]'.format(pname))
                    self.collectorjobs[pname].terminate()
                    self.collectorjobs[pname].terminate()
                    self.collectorjobs[jname].join()
                    del self.collectorjobs[pname]
                    logging.warning('pg-stat-profiler : Disable profile execution success : [{}]'.format(pname))
                # start collector process if crashed, new or newly-enabled via api
                if pname not in self.collectorjobs and profile.getStatus() == 'enabled':
                    logging.warning('pg-stat-profiler : Enabling profile collection : [{}]'.format(pname))
                    thiscollector = collector(pname,profile)
                    thisprocess = multiprocessing.Process(target=thiscollector.run,args=(profilesqueue,loggingqueue))
                    self.collectorjobs[pname] = thisprocess
                    self.collectorjobs[pname].start()
                    logging.warning('pg-stat-profiler : Enable profile collection success : [{}]'.format(pname))
            for jname in list(self.collectorjobs.keys()):
                # stop existing collector process if deleted via api
                #logging.warning('pg-stat-profiler : Reviewing profile collection : [{}]'.format(jname))
                if jname not in self.profilestore.getProfiles():
                    logging.warning('pg-stat-profiler : Disabling profile collection : [{}]'.format(jname))
                    self.collectorjobs[jname].terminate()
                    self.collectorjobs[jname].join()
                    del self.collectorjobs[jname]
                    logging.warning('pg-stat-profiler : Disable profile execution success : [{}]'.format(jname))
            time.sleep(10)
        except Exception as e:
            logging.warning('pg-stat-profiler : profilesupervisor unexpected error : [{}]'.format(str(e)))


         
