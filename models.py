from django.db import models

# Create your models here.

class WebApiTestItem(models.Model):
    field_1 = models.CharField(blank=False, null=False, max_length=255)
    field_2 = models.CharField(blank=False, null=False, max_length=255)
    field_3 = models.CharField(blank=False, null=False, max_length=255)
    field_4 = models.CharField(blank=False, null=False, max_length=255)
    field_5 = models.CharField(blank=False, null=False, max_length=255)
    
    class Meta:
        db_table = 'test_web_api_storage'
        verbose_name = 'Web Api Test Item'
        verbose_name_plural = 'Web Api Test Items'
