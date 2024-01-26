import unittest
import uuid
import os
from unittest.mock import MagicMock
from flask import request
from postgres_stat_profiler.api_auth.api_request import api_request

class TestApi_auth(unittest.TestCase):

    def test_init(self):
        randomstring = uuid.uuid1()
        mock_request = MagicMock(authorization = randomstring)
        req = api_request(mock_request)
        key = req.getRequestkey() 
        assert key == randomstring
        assert req.getValid()

    def test_missingAuth(self):
        mock_request = MagicMock(authorization = None)
        req = api_request(mock_request)
        key = req.getRequestkey() 
        assert not req.getValid()