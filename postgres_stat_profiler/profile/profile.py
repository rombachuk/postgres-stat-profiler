import logging
import logging.handlers
import json
import time
from flask import request
from postgres_stat_profiler.config.connection import connection
from postgres_stat_profiler.collector.reportDatabase import reportDatabase
from postgres_stat_profiler.collector.monitoredDatabase import monitoredDatabase
from postgres_stat_profiler.collector.collector import collector

class profile:
  
  def __init__(self,data):
     self.valid = False
     if 'name' in data:
        self.name = data['name']
        if self._setStatuses(data) and self._setConnections(data):
           self.valid = True
 
  def getName(self):
      return self.name
  
  def getStatus(self):
      return self.status
  
  def getMonitoredDBstatus(self):
      return self.monitordbstatus
     
  def getReportDBstatus(self): 
      return self.reportdbstatus
     
  def getValid(self):
     return self.valid
  
  def getAllDetails(self):
     return self._getDetails(self.monitored_connection.getAllDetails(),self.report_connection.getAllDetails())
  
  # credentials never exposed over GET from api
  def getApiDetails(self):
     return self._getDetails(self.monitored_connection.getApiDetails(),self.report_connection.getApiDetails())

  def _getDetails(self,monitoredconndetails,reportconndetails):
     try: 
        return "{{ 'name' : '{}', 'status': '{}', 'monitored_connection' : {{{}}}, 'monitordbstatus' : '{}', 'report_connection' : {{{}}}, 'reportdbstatus' : '{}' }}".\
             format(self.name, str(self.status),\
             monitoredconndetails, self.getMonitoredDBstatus(),\
             reportconndetails, self.getReportDBstatus())
     except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-getDetails error : [{}]'.format(str(e)))
     

  def update(self,data):
     try:
           if data:
             if 'status' in data and ((data['status'] == u'disabled') or (data['status'] == u'enabled')):
               self.status = data['status']
             if 'report_connection' in data:
               self.report_connection.update(data['report_connection'])
             if 'reportdbstatus'in data:
               self.reportdbstatus = data['reportdbstatus']
             if 'monitored_connection' in data:
               self.monitored_connection.update(data['monitored_connection'])  
             if 'monitordbstatus'in data:
               self.monitordbstatus = data['monitordbstatus']
             self.valid = True
           return True        
     except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-update : [{}]'.format(str(e)))
        self.valid = False
        return False
     
  def run(self, profilesqueue, loggingqueue):
       try: 
        h = logging.handlers.QueueHandler(loggingqueue) 
        logger = logging.getLogger()
        logger.addHandler(h)
        logging.warn('pg_stat_profiler: profile data collector [{}] started'.format(self.name))
        check_interval = 10
        collect_interval = 60
        counter = 0
        while True:
           # check status before trying collection (every check_interval)
           coll = collector(self.name,self.monitored_connection,self.report_connection)
           self.reportdbstatus = coll.getReportDBstatus()
           self.monitordbstatus = coll.getMonitoredDBstatus()
           # pass result back via queue to grandparent main process - which updates the (persistent, encrypted) profilesfile
           result = {"name": self.name, "reportdbstatus": self.reportdbstatus, "monitordbstatus": self.monitordbstatus }
           profilesqueue.put(result)

           # attempt collection (every connection interval)
           counter = counter+1
           if check_interval*counter > collect_interval:
              coll.collect()
              counter = 0
           time.sleep(10.0)
           
       except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-run error : [{}]'.format(str(e)))
     
  def _setConnections(self,data):
     try:
           if data and 'report_connection' in data and 'monitored_connection' in data:
              self.report_connection = connection(data['report_connection'])
              self.monitored_connection = connection(data['monitored_connection'])
              if self.report_connection.getValid() and self.monitored_connection.getValid():
                    return True
           return False
     except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-setConnections error : [{}]'.format(str(e)))
        return False

  def _setStatuses(self,data):
     try:
           if data and 'status' in data :
              self.status = data['status']
           if not hasattr(self,'status'):
              self.status = 'disabled'
           if not hasattr(self,'monitordbstatus'):
              self.monitordbstatus = 'unknown'
           if not hasattr(self,'reportdbstatus'):
              self.reportdbstatus = 'unknown'
           return True
     except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-setStatus error : [{}]'.format(str(e)))
        return False

  def __str__(self):
        return str(self.__dict__)  

