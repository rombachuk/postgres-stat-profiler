import os
import logging
import psycopg
from postgres_stat_profiler.collection.reportschema import reportschema


class reportDatabase():

    def __init__(self,connstring):
        self.connstring = connstring
        self.schema = reportschema()
        self._checkStatus()

    def setConfig(self,config):
        self.config = config

    def getConnstring(self):
        return self.connstring

    def getStatus(self):
        return self.status

    def _checkStatus(self):
        try: 
           if not hasattr(self,'status'):
              self.status = 'new'
           with psycopg.connect(self.connstring) as conn:
             with conn.cursor() as cur:
                testcommand = self.schema.getTestCommand()
                cur.execute(testcommand)   
                self.status = 'initialised'
        except Exception as e:
           logging.warning('pg-stat-profiler : report database checkstatus : table missing or not granted[{}]'.format(str(e)))
           # check for schema missing and initialise it
           error = str(e)
           if 'does not exist' in error:
                 self._initialise()
           else:
              self.status = 'failed'
             
    def _initialise(self):
        try:
          if self.status == 'failed':
             logging.warning('pg-stat-profiler : report database : initialise attempt on failed database : please grant access to the configured user and retry')
             return
          else:
           with psycopg.connect(self.connstring) as conn:
            with conn.cursor() as cur:
              logging.warning('pg-stat-profiler : report database : initialise started')
              for command in self.schema.getCreateSchema():
                 logging.warning('pg-stat-profiler : report database : command [{}]'.format(command[:50]))
                 try:
                   # connection autocommit is false. postgres does not autocommit DDL
                   cur.execute(command)
                   cur.execute(u'COMMIT')
                 except Exception as e:
                   # ignore errors on drop as schema may not exist
                   cur.execute(u'ROLLBACK')
                   if not 'DROP' in command:
                      logging.warning('pg-stat-profiler : reportdatabase initialise : command [{}] error [{}]'.format(command,str(e)))
                      self.status = 'failed'
                      return
              for command in self.schema.getCreateTables():
                 logging.warning('pg-stat-profiler : report database : command [{}]'.format(command[:50]))
                 try:
                   # connection autocommit is false. postgres does not autocommit DDL
                   cur.execute(command)
                   cur.execute(u'COMMIT')
                 except Exception as e:
                   # ignore errors on drop as table may not exist
                   cur.execute(u'ROLLBACK')
                   if not 'DROP' in command:
                      logging.warning('pg-stat-profiler : reportdatabase initialise : command [{}] error [{}]'.format(command,str(e)))
                      self.status = 'failed'
                      return
              for command in self.schema.getCreateIndexes():
                 logging.warning('pg-stat-profiler : report database : command [{}]'.format(command[:50]))
                 try:
                   # connection autocommit is false. postgres does not autocommit DDL. Index created with IF NOT EXISTS
                   # status is not set to 'failed' on index failure
                   cur.execute(command)
                   cur.execute(u'COMMIT')
                 except Exception as e:
                   cur.execute(u'ROLLBACK')
                   logging.warning('pg-stat-profiler : reportdatabase initialise : command [{}] error [{}]'.format(command,str(e)))
              logging.warning('pg-stat-profiler : report database : initialise completed')
            self.status = 'initialised'
        except Exception as e:
           logging.warn('pg-stat-profiler : reportdatabase initialise : Unexpected error [{}]'.format(str(e)))
           self.status = 'failed'