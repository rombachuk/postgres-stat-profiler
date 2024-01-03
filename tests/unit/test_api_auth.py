import unittest
import logging
import uuid
import os
from unittest.mock import MagicMock
from flask import request
from postgres_stat_profiler.api_auth.api_auth import api_auth

os.environ['PG_STAT_PROFILER_LOGBASE'] = os.path.expanduser('~/Documents/GitHub/postgres_stat_profiler/postgres_stat_profiler/resources/log')
logfilename = os.path.join(os.getenv(u'PG_STAT_PROFILER_LOGBASE'),u"pg-stat-profiler-unittest.log")
logging.basicConfig(filename = logfilename, level=logging.WARNING,
                    format='%(asctime)s[%(funcName)-5s] (%(processName)-10s) %(message)s',
                    )

class TestApi_auth(unittest.TestCase):

    def test_init(self):
        randomstring = uuid.uuid1()
        mock_request = MagicMock(authorization = randomstring)
        auth = api_auth(mock_request)
        key = auth.getRequestkey() 
        assert key == randomstring
        assert auth.getValid()

    def test_missingAuth(self):
        mock_request = MagicMock(authorization = None)
        auth = api_auth(mock_request)
        key = auth.getRequestkey() 
        assert not auth.getValid()