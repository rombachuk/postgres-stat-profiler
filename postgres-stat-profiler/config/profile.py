import logging
import json
import time
from flask import request
from config.connection import connection

class profile:
 
  def __init__(self,data):
     self.valid = False
     if 'name' in data:
        self.name = data['name']
        if self._setConnections(data) and self._setStatus(data):
           self.valid = True
 
  def getName(self):
     return self.name
  
  def getStatus(self):
     return self.status
  
  def getValid(self):
     return self.valid
  
  def getAllDetails(self):
     try:
        return ('{{ "name" : "{}", "status" : "{}", "monitored_connection" : {{{}}}, "report_connection" : {{{}}}}}'.\
             format(self.name, str(self.status),\
             self.monitoredconnection.getAllDetails(), \
             self.reportconnection.getAllDetails()))
     except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-getApiDetails error : [{}]'.format(str(e)))
     
  
  # credentials never exposed over GET from api
  def getApiDetails(self):
     try: 
        return ("{{ 'name' : '{}', 'status' : '{}', 'monitored_connection' : {{{}}}, 'report_connection' : {{{}}} }}".\
             format(self.name, str(self.status),\
             self.monitoredconnection.getApiDetails(), \
             self.reportconnection.getApiDetails()))
     except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-getApiDetails error : [{}]'.format(str(e)))

  def update(self,data):
     try:
           if data:
             if 'status' in data and ((data['status'] == u'disabled') or (data['status'] == u'enabled')):
               self.status = data['status']
             if 'report_connection' in data:
               self.reportconnection.update(data['report_connection'])
             if 'monitored_connection' in data:
               self.monitoredconnection.update(data['monitored_connection'])  
             self.valid = True
           return True        
     except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-update : [{}]'.format(str(e)))
        self.valid = False
        return False
     
  def run(self):
       try: 
        while True:
           logging.warning('pg-stat-profiler : profile [{}] running tick...'.format(self.name))
           time.sleep(1.0)
           
       except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-run error : [{}]'.format(str(e)))
     
  def _setConnections(self,data):
     try:
           if data and 'report_connection' in data and 'monitored_connection' in data:
              self.reportconnection = connection(data['report_connection'])
              if self.reportconnection.getValid():
                 self.monitoredconnection = connection(data['monitored_connection'])
                 if self.monitoredconnection.getValid():
                    return True
           return False
     except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-setConnections error : [{}]'.format(str(e)))
        return False

  def _setStatus(self,data):
     try:
           if data and 'status' in data :
              self.status = data['status']
           else:
              self.status = 'disabled'
           return True
     except Exception as e:
        logging.warning('pg-stat-profiler : unexpected profile-setConnections error : [{}]'.format(str(e)))
        return False

  def __str__(self):
        return str(self.__dict__)  

