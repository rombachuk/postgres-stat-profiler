import unittest
import logging
import os
from unittest.mock import MagicMock
from flask import request
from postgres_stat_profiler.api_auth import api_auth

os.environ['PG_STAT_PROFILER_LOGBASE'] = '/Users/y7kwh/Documents/GitHub/postgres-stat-profiler/postgres_stat_profiler/resources/log'
logfilename = os.path.join(os.getenv(u'PG_STAT_PROFILER_LOGBASE'),u"pg-stat-profiler-unittest.log")
logging.basicConfig(filename = logfilename, level=logging.WARNING,
                    format='%(asctime)s[%(funcName)-5s] (%(processName)-10s) %(message)s',
                    )

class TestApi_auth(unittest.TestCase):

    def test_init(self):
        mock_request = MagicMock(authorization = u'6acecbcbfa594228bceeff21b701838f804282d581894dff918812c76b232ee2')
        auth = api_auth(mock_request)
        key = auth.getRequestkey() 
        assert key == u'6acecbcbfa594228bceeff21b701838f804282d581894dff918812c76b232ee2'
        assert auth.getValid()

    def test_missingAuth(self):
        mock_request = MagicMock(authorization = None)
        auth = api_auth(mock_request)
        key = auth.getRequestkey() 
        assert not auth.getValid()