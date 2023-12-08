import os
import logging
import psycopg

class reportDatabase():

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
                result = cur.execute("SELECT * FROM test LIMIT 1")   
                self.status = 'initialised'
        except Exception as e:
           logging.warn('pg-stat-profiler : report database getstatus : Unexpected error [{}]'.format(str(e)))
           self.status = 'new'
           self._initialise()
             
    def _initialise(self):
        try:
           with psycopg.connect(self.connstring) as conn:
            with conn.cursor() as cur:
                cur.execute("""
            CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """)
            self.status = 'initialised'
        except Exception as e:
           logging.warn('pg-stat-profiler : reportdatabase initialise : Unexpected error [{}]'.format(str(e)))
           self._initialise()
           self.status = 'failed'