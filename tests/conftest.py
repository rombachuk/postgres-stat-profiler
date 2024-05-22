import pytest
import os
import json
import logging
from postgres_stat_profiler import create_app
from postgres_stat_profiler.helpers.env_helper import fetch_env_allow_empty

@pytest.fixture(scope='module')
def test_apiroot():
    return u'/_api/v1.0'

@pytest.fixture(scope='module')
def test_client():
    envprofilerbase = os.getenv(u'PG_STAT_PROFILER_BASE')
    if not envprofilerbase:
       installbase = os.getcwd()
    else:
       installbase = os.path.expandvars(envprofilerbase)
    secbase = os.path.join(installbase,u'postgres_stat_profiler/resources/sec')
    keystorefile = os.path.join(secbase,u'.pg-stat-profiler.keystr')
    profilesfile = os.path.join(secbase,u'.pg-stat-profiler.prof')
    if os.path.isfile(keystorefile):
           os.remove(keystorefile)
    if os.path.isfile(profilesfile):
           os.remove(profilesfile)
    

    flask_app = create_app()
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def test_apikeyheader(test_client,test_apiroot):
    try:
      # generate a apikeyheader for use in functional testing
      # use the apikeygen_secret to find an apikey
      api_secret = os.getenv(u'PG_STAT_PROFILER_APIKEYGEN_SECRET')
      headers = {"Authorization" : '{}'.format(api_secret)}
      response = test_client.get('{}/apikeys'.format(test_apiroot),headers=headers)
      data = json.loads(response.data)
      ckeys = json.loads(data['apikeys'].replace("'",'"'))
      apikeyheader = {"Authorization" : '{}'.format(ckeys[0])}
      return apikeyheader
    except Exception as e:
      logging.warning('pg_stat_profiler : Fixture failure : Failed to fetch apikey')
      return None

@pytest.fixture(scope='module')
def test_profilename():
    return u'lometricscheck1'

@pytest.fixture(scope='module')
def test_profile(test_profilename):
    try: 
      installbase = fetch_env_allow_empty(u'PG_STAT_PROFILER_BASE')
      samplebase = os.path.join(installbase,u'postgres_stat_profiler/resources/samples')
      testprofilefile = os.path.join(samplebase,u'{}.json'.format(test_profilename))
      if os.path.isfile(testprofilefile): 
        tpf = open(testprofilefile,'r')
        contents = tpf.read()
        tpf.close
        return contents
    except Exception as e:
      logging.warning('pg_stat_profiler : Fixture failure : Failed to fetch profile contents')
      return None