import urllib, urllib2, socket
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import simplejson

headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
timeout = 10 #connection timeout in seconds
socket.setdefaulttimeout(timeout)

class WebApiClient(object):    
    def _request(self, url_path, post_data, extras_list=None):
        post_data.update({'L': settings.WEB_API_SERVER_LOGIN, 'P': settings.WEB_API_SERVER_PASSWORD})
        if extras_list:
            post_data.update({'extras': " ".join(extras_list)})
        url = settings.WEB_API_SERVER_MAIN_URL + url_path
        data = urllib.urlencode(post_data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        return response.read()
        
    def query_filter(self, app_label, model_name, filter_dict, extras_list=None):
        request_url_path = reverse('web_api_handler_filter_url', kwargs={'app_label': app_label, 'model_name': model_name})
        response = self._request(request_url_path, filter_dict, extras_list)
        return simplejson.loads(response)
