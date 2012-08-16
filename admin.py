from django.contrib import admin
from django_model_web_api.models import WebApiTestItem
from django.conf import settings

if settings.DEBUG and settings.WEB_API_MODE == 'server':
    class WebApiTestItemAdmin(admin.ModelAdmin):
        pass
    admin.site.register(WebApiTestItem, WebApiTestItemAdmin)
