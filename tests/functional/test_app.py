import os
import json
import logging
import unittest


def test_welcome(test_client,test_apikeyheader):
    
    response = test_client.get('/_api/v1.0',headers=test_apikeyheader)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'postgres-stat-profiler' in data
    assert 'welcome' in data['postgres-stat-profiler']