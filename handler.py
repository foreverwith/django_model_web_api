from django.conf import settings
from django.utils import simplejson
from django.http import HttpResponse
from django.db.models.loading import get_model
from django.core import serializers

class WebApiHandler(object):
    def auth(self):
        authenticated = True
        return authenticated
        
    def _success_response(self, serialized_result):
        data = '{"STATUS": "OK", "RESULT": %s}' % serialized_result
        return HttpResponse(data, mimetype="application/json")
        
    def _fail_response(self, error_message):
        data = {'ERROR': error_message}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        
    def query(self, model_cls, method_name, *args, **kwargs):    
        try:
            func = getattr(model_cls.objects, method_name)
            result = func(*args, **kwargs)
        except Exception as e:
            return self._fail_response(str(e))
        else:
            return self._success_response(result)
        
    def query_filter(self, app_label, model_name, filter_dict, extras_str=None):
        '''
        extras is an argument that consists of space separeted model fields/props which shall be extracted from model instances
        '''
        auth_login = filter_dict.pop('L')
        auth_password = filter_dict.pop('P')
        
        if auth_login != settings.WEB_API_SERVER_LOGIN or auth_password != settings.WEB_API_SERVER_PASSWORD:
            return self._fail_response('Authentication failed!')
            
        extras = extras_str.split(' ') if extras_str else []
        
        try:
            model_cls = get_model(app_label, model_name)
            query_set = model_cls.objects.filter(**filter_dict)
        except Exception, e:
            return self._fail_response(str(e))
        data = serializers.serialize("json", query_set, indent=2, use_natural_keys=True, extras=extras)
        return self._success_response(data)
