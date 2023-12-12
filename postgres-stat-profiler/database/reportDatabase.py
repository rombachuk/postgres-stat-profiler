import os
import logging
import psycopg
from database.reportschema import reportschema

class reportDatabase():

    def __init__(self,connstring):
        self.connstring = connstring
        self.schema = reportschema()
        self._checkStatus()

    def setConfig(self,config):
        self.config = config

    def getStatus(self):
        return self.status

    def _checkStatus(self):
        try: 
           with psycopg.connect(self.connstring) as conn:
             with conn.cursor() as cur:
                testcommand = self.schema.getTestCommand()
                cur.execute(testcommand)   
                self.status = 'initialised'
        except Exception as e:
           logging.warn('pg-stat-profiler : report database getstatus : Unexpected error [{}]'.format(str(e)))
           # attribute will be absent on first run
           if not hasattr(self,'status'):
              self.status = 'new'
              self._initialise()
           else:
              self.status = 'failed'
             
    def _initialise(self):
        try:
          if not self.status == 'failed':
           with psycopg.connect(self.connstring) as conn:
            with conn.cursor() as cur:
              logging.warn('pg-stat-profiler : report database : initialise started')
              for command in self.schema.getCreateTables():
                 logging.warn('pg-stat-profiler : report database : command [{}]'.format(command[:50]))
                 try:
                   # connection autocommit is false. postgres does not autocommit DDL
                   cur.execute(command)
                   cur.execute(u'COMMIT')
                 except Exception as e:
                   # ignore errors on drop as table may not exist
                   cur.execute(u'ROLLBACK')
                   if not 'DROP' in command:
                      logging.warn('pg-stat-profiler : reportdatabase initialise : command [{}] error [{}]'.format(command,str(e)))
                      self.status = 'failed'
                      return
              logging.warn('pg-stat-profiler : report database : initialise completed')
            self.status = 'initialised'
        except Exception as e:
           logging.warn('pg-stat-profiler : reportdatabase initialise : Unexpected error [{}]'.format(str(e)))
           self.status = 'failed'