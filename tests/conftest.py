import pytest
import os
import json
import logging
from postgres_stat_profiler import create_app

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
def test_apikeyheader(test_client):
    try:
      # generate a apikeyheader for use in functional testing
      # use the api_secret to find an apikey
      api_secret = os.getenv(u'PG_STAT_PROFILER_SECRET')
      headers = {"Authorization" : '{}'.format(api_secret)}
      response = test_client.get('/_api/v1.0/apikeys',headers=headers)
      data = json.loads(response.data)
      ckeys = json.loads(data['apikeys'].replace("'",'"'))
      apikeyheader = {"Authorization" : '{}'.format(ckeys[0])}
      return apikeyheader
    except Exception as e:
      logging.warning('pg_stat_profiler : Fixture failure : Failed to fetch apikey')
      return None

