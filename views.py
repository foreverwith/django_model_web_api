from django_model_web_api.handler import WebApiHandler
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

def request_post_to_dict(request_post):
    post_data = {}
    for k, v in request_post.items():
        post_data.update({k: v})
    return post_data

@csrf_exempt
def filter(request, app_label, model_name):
    api_handler = WebApiHandler()
    post_data = request_post_to_dict(request.POST)
    print post_data
    extras = post_data.pop('extras', None)
    print extras
    return api_handler.query_filter(app_label, model_name, post_data, extras)
