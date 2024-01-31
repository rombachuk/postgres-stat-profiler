import os
import json
import logging
import unittest
import uuid

def test_welcome(test_client,test_apikeyheader):
    response = test_client.get('/_api/v1.0',headers=test_apikeyheader)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'postgres-stat-profiler' in data
    assert 'welcome' in data['postgres-stat-profiler']

def test_welcome_invalidkey(test_client):
    randomkey = '{}{}'.format(uuid.uuid4().hex,uuid.uuid4().hex)
    apikeyheader = {"Authorization" : '{}'.format(randomkey)}
    response = test_client.get('/_api/v1.0',headers=apikeyheader)
    assert response.status_code == 401

def test_empty_profiles(test_client,test_apikeyheader):
    response = test_client.get('/_api/v1.0/profiles',headers=test_apikeyheader)
    assert response.status_code == 404

