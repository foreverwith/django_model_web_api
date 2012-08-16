import django
if int("%s%s" % (django.VERSION[0], django.VERSION[1])) > 13:
    from django.conf.urls import patterns, include, url
else:
    from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^filter/(?P<app_label>[\d\w_]+)/(?P<model_name>[\d\w_]+)/', 'web_api.views.filter', name='web_api_handler_filter_url'),
)
