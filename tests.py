from django_webtest import WebTest
from django.conf import settings
from django.core.urlresolvers import reverse
from django_model_web_api.handler import WebApiHandler
from django_model_web_api.client import WebApiClient
from django.utils import simplejson
import random

if settings.WEB_API_MODE == 'server':
    class WebApiHandlerTest(WebTest):
        setup_auth = False
        fixtures = ['test_data.json']
        
        def setUp(self):
            self.auth_ok_data = {'L': settings.WEB_API_SERVER_LOGIN, 'P': settings.WEB_API_SERVER_PASSWORD}
            self.auth_fail_data = {'L': random.randrange(100000, 999999), 'P': random.randrange(100000, 999999)}
            
        def test_auth_fail(self):
            post_data = {"pk": 1}
            post_data.update(self.auth_fail_data)
            response = self.app.post(reverse('web_api_handler_filter_url', kwargs={'app_label': 'web_api', 'model_name': 'WebApiTestItem'}), post_data)
            json_decoded = simplejson.loads(response.body)
            self.assertEqual(json_decoded.has_key('ERROR'), True)
            self.assertEqual('Authentication failed!' in json_decoded['ERROR'], True)
        
        def test_query_filter_url_ok(self):
            post_data = {"pk": 1}
            post_data.update(self.auth_ok_data)
            response = self.app.post(reverse('web_api_handler_filter_url', kwargs={'app_label': 'web_api', 'model_name': 'WebApiTestItem'}), post_data)
            json_decoded = simplejson.loads(response.body)
            self.assertEqual(json_decoded.has_key('STATUS'), True)
            self.assertEqual(json_decoded['STATUS'], 'OK')
        
        def test_query_filter_url_error(self):
            post_data = {"opopop": 1000}
            post_data.update(self.auth_ok_data)
            response = self.app.post(reverse('web_api_handler_filter_url', kwargs={'app_label': 'web_api', 'model_name': 'WebApiTestItem'}), post_data)
            json_decoded = simplejson.loads(response.body)
            self.assertEqual(json_decoded.has_key('ERROR'), True)

if settings.WEB_API_MODE == 'client':        
    class WebApiClientTest(WebTest):
        setup_auth = False
        fixtures = ['test_data.json']
        
        def setUp(self):
            self.web_api_client = WebApiClient()
        
        def test_query_filter_ok(self):
            result = self.web_api_client.query_filter(app_label='web_api', model_name='WebApiTestItem', filter_dict={"pk": 1})
            self.assertEqual(result['STATUS'], 'OK')
            
        def test_query_filter_error(self):
            result = self.web_api_client.query_filter(app_label='web_api', model_name='WebApiTestItem2', filter_dict={"pk": random.randrange(100000, 999999)})
            self.assertEqual(result.has_key('ERROR'), True)
