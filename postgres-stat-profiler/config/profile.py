import logging
import json
import time
from flask import request
from config.connection import connection
from database.reportDatabase import reportDatabase
from database.monitoredDatabase import monitoredDatabase

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
             if 'monitored_connection' in data:
               self.monitored_connection.update(data['monitored_connection'])  
             self.valid = True
           return True        
     except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-update : [{}]'.format(str(e)))
        self.valid = False
        return False
     
  def run(self):
       try: 
        while True:
           repdb = reportDatabase(self.report_connection.getConnectionString())
           self.reportdbstatus = repdb.getStatus()
           mondb = monitoredDatabase(self.monitored_connection.getConnectionString())
           self.monitordbstatus = mondb.getStatus()
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

