from django.db import models

# Create your models here.

class JudgeDetail(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
class Job(models.Model):
    title = models.CharField(max_length=255, default='N/A')
    company = models.CharField(max_length=255, default='N/A')
    link = models.CharField(max_length=255, null=True)
    salary = models.CharField(max_length=255, null=True)
    published_date = models.CharField(max_length=255, null=True)
    unique_id = models.CharField(max_length=255, null=True)

