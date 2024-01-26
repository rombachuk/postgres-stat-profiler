import unittest
import uuid
import os
from unittest.mock import MagicMock
from flask import request
from postgres_stat_profiler.api_auth.api_keystore import api_keystore

class TestApi_keystore(unittest.TestCase):
    def setUp(self):
        self.unittest_keystorefile = os.path.join(u'/tmp',u'.pg-stat-profiler-unittest.keystr')

    def tearDown(self):
        os.remove(self.unittest_keystorefile)

    def test_init(self):
        mock_secret = uuid.uuid1().hex
        keystore = api_keystore(mock_secret,self.unittest_keystorefile)
        for i in range(0,5):
          key = keystore.getApiKey(i)
          self.assertNotEqual(key,None)
        assert keystore.checkKeyfile()

