import os
import json
import logging
import unittest
import uuid
from postgres_stat_profiler.helpers.env_helper import fetch_env_allow_empty

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


def test_create_profile(test_client,test_apikeyheader):
    testprofilename = u'lometricscheck1'
    installbase = fetch_env_allow_empty(u'PG_STAT_PROFILER_BASE')
    samplebase = os.path.join(installbase,u'postgres_stat_profiler/resources/samples')
    testprofilefile = os.path.join(samplebase,u'{}.json'.format(testprofilename))
    if os.path.isfile(testprofilefile): 
      tpf = open(testprofilefile,'r')
      contents = tpf.read()
      tpf.close
      headers = test_apikeyheader
      headers['Content-Type'] = u"application/json"
      response = test_client.post('/_api/v1.0/profiles/{}'.format(testprofilename),headers=headers,json=json.loads(contents))
      assert response.status_code == 200
      data = json.loads(response.data)
      assert 'result' in data
      assert 'ok' in data['result']
    else:
      assert False

def test_get_profile(test_client, test_apikeyheader):
    testprofilename = u'lometricscheck1'
    response = test_client.get('/_api/v1.0/profiles/{}'.format(testprofilename),headers=test_apikeyheader)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    assert 'name' in data['result']
    result = json.loads(data['result'])
    assert testprofilename in result['name']


def test_get_all_profiles(test_client, test_apikeyheader):
    testprofilename = u'lometricscheck1'
    response = test_client.get('/_api/v1.0/profiles',headers=test_apikeyheader)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    result = json.loads(data['result'][0])
    assert testprofilename in result['name']
                               

