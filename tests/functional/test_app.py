from postgres_stat_profiler.app import app

def test_get_api():
    response = app.test_client().get('/api/v1.0',headers=u'')