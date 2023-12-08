import os
import logging
import psycopg

class monitoredDatabase():

    def __init__(self,connstring):
        self.connstring = connstring
        self._checkStatus()

    def setConfig(self,config):
        self.config = config

    def getStatus(self):
        return self.status

    def _checkStatus(self):
        try: 
           with psycopg.connect(self.connstring) as conn:
             with conn.cursor() as cur:
                result = cur.execute("SELECT * FROM pg_stat_statements LIMIT 1")   
                self.status = 'operational'
        except Exception as e:
           logging.warn('pg-stat-profiler : monitored database getstatus : Unexpected error [{}]'.format(str(e)))
           self.status = 'missing-pg-stat-statements'
