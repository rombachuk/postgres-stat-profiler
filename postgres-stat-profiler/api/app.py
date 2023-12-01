from flask import Flask, abort, jsonify, make_response, request, Response
from functools import wraps
import json
import datetime
import sys
import logging

app = Flask(__name__)

logfilename = "log/pg-stat-profiler.log"

logging.basicConfig(filename = logfilename, level=logging.WARNING,
                    format='%(asctime)s[%(funcName)-5s] (%(processName)-10s) %(message)s',
                    )

if __name__ == '__main__':
 try:
 
   logging.warn("Startup : Postgres Stat Profiler")
   app.run()
 except Exception as e:
  logging.warn("Exception Shutdown : Postgres Stat Profiler: Error ["+str(e)+"]")
