from django.db import models

# Create your models here.


class Job(models.Model):
    title = models.CharField(max_length=255, default='N/A')
    company = models.CharField(max_length=255, default='N/A')
    link = models.CharField(max_length=255, null=True)
    salary = models.CharField(max_length=255, null=True)
    published_date = models.CharField(max_length=255, null=True)
