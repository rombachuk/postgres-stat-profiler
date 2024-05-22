import os
import json
import logging
import unittest
import uuid
from postgres_stat_profiler.helpers.env_helper import fetch_env_allow_empty

def test_welcome(test_client,test_apikeyheader,test_apiroot):
    response = test_client.get(test_apiroot,headers=test_apikeyheader)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'postgres-stat-profiler' in data
    assert 'welcome' in data['postgres-stat-profiler']

def test_welcome_invalidkey(test_client,test_apiroot):
    randomkey = '{}{}'.format(uuid.uuid4().hex,uuid.uuid4().hex)
    apikeyheader = {"Authorization" : '{}'.format(randomkey)}
    response = test_client.get(test_apiroot,headers=apikeyheader)
    assert response.status_code == 401

def test_empty_profiles(test_client,test_apikeyheader,test_apiroot):
    response = test_client.get('{}/profiles'.format(test_apiroot),headers=test_apikeyheader)
    assert response.status_code == 404

def test_create_profile(test_client,test_apikeyheader,test_profilename,test_profile,test_apiroot):
    headers = test_apikeyheader
    headers['Content-Type'] = u"application/json"
    response = test_client.post('{}/profiles/{}'.format(test_apiroot,test_profilename),headers=headers,json=json.loads(test_profile))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    assert 'ok' in data['result']

def test_create_profile_already_exists(test_client,test_apikeyheader,test_profilename,test_profile,test_apiroot):
    headers = test_apikeyheader
    headers['Content-Type'] = u"application/json"
    response = test_client.post('{}/profiles/{}'.format(test_apiroot,test_profilename),headers=headers,json=json.loads(test_profile))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    assert 'error' in data['result']

def test_get_profile(test_client,test_apikeyheader,test_profilename,test_apiroot):
    response = test_client.get('{}/profiles/{}'.format(test_apiroot,test_profilename),headers=test_apikeyheader)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    assert 'name' in data['result']
    result = json.loads(data['result'])
    assert test_profilename in result['name']

def test_get_all_profiles(test_client, test_apikeyheader, test_profilename, test_apiroot):
    response = test_client.get('{}/profiles'.format(test_apiroot),headers=test_apikeyheader)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    result = json.loads(data['result'][0])
    assert test_profilename in result['name']

def test_statusupdate_enable_profile(test_client, test_apikeyheader, test_profilename, test_apiroot):
    headers = test_apikeyheader
    headers['Content-Type'] = u"application/json"
    status = u'{"status":"enabled"}'
    response = test_client.put('{}/profiles/{}'.format(test_apiroot,test_profilename),headers=headers,json=json.loads(status))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    assert 'ok' in data['result']

def test_statusupdate_disable_profile(test_client, test_apikeyheader, test_profilename, test_apiroot):
    headers = test_apikeyheader
    headers['Content-Type'] = u"application/json"
    status = u'{"status":"disabled"}'
    response = test_client.put('{}/profiles/{}'.format(test_apiroot,test_profilename),headers=headers,json=json.loads(status))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    assert 'ok' in data['result']
                               
def test_statusupdate_profile_invalid_value(test_client, test_apikeyheader, test_profilename, test_apiroot):
    headers = test_apikeyheader
    headers['Content-Type'] = u"application/json"
    status = u'{"status":"illegal"}'
    response = test_client.put('{}/profiles/{}'.format(test_apiroot,test_profilename),headers=headers,json=json.loads(status))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    assert 'error' in data['result']

def test_delete_profile(test_client,test_apikeyheader,test_profilename,test_apiroot):
    response = test_client.delete('{}/profiles/{}'.format(test_apiroot,test_profilename),headers=test_apikeyheader)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    assert 'ok' in data['result']
    response = test_client.get('{}/profiles/{}'.format(test_apiroot,test_profilename),headers=test_apikeyheader)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Not Found' in data['error']
   
