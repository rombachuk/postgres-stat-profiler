import unittest
import uuid
import os
from unittest.mock import MagicMock
from flask import request
from postgres_stat_profiler.api_auth.api_request import api_auth

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