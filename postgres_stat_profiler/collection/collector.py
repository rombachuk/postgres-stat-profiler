import time
import logging
from postgres_stat_profiler.collection.postgresCollector import postgrescollector

class collector:

    def __init__(self, name, profile):
        self.profilename = name
        self.profile = profile
        self.type = self.profile.getMonitoredDBconnection().getType()
        self.status = u'new'
        self._checkValid()

    def _checkValid(self):
        if self.type == u'postgresql':
           self.valid = True
        else:
           self.valid = False

    def getValid(self):
        return self.valid

    def run(self, profilesqueue, loggingqueue):
       try: 
        h = logging.handlers.QueueHandler(loggingqueue) 
        logger = logging.getLogger()
        logger.addHandler(h)
        logging.warn('pg_stat_profiler: profile data collector [{}] initialising'.format(self.profilename))
        self.status = u'initialising'
        sleep_interval = 60.0
        starttime = time.monotonic()
        while self.valid:
        
           if self.type != 'postgresql':
              logging.warning('pg-stat-profiler :  collector-run error : profile [{}] unsupported monitordb type [{}]'.format(self.profilename, self.type))
           else:
              dbcollector = postgrescollector(self.profile)
           # report status to parent processes to allow api read of status      
              reportdbstatus = dbcollector.getReportDBstatus()
              monitordbstatus = dbcollector.getMonitoredDBstatus()
           # pass result back via queue to grandparent main process - which updates the (persistent, encrypted) profilesfile
              result = {"name": self.profilename, "reportdbstatus": reportdbstatus, "monitordbstatus": monitordbstatus }
              profilesqueue.put(result)
              if monitordbstatus == u'operational' and reportdbstatus == u'initialised':
                if self.status != u'started':
                   logging.warn('pg_stat_profiler: profile data collector [{}] has detected valid databases'.format(self.profilename))
                   logging.warn('pg_stat_profiler: profile data collector [{}] collection active'.format(self.profilename))
                   self.status = u'started'
                dbcollector.collect()
           time.sleep(sleep_interval - ((time.monotonic() - starttime) % sleep_interval))
           self._checkValid()
           
       except Exception as e:
        logging.warning('pg-stat-profiler : unexpected collector-run error : [{}]'.format(str(e)))
     

   