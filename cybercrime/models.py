from django.db import models

class PhishingData(models.Model):
    url_length          = models.IntegerField()
    has_ip              = models.BooleanField(default=False)
    suspicious_keywords = models.IntegerField(default=0)
    has_https           = models.BooleanField(default=True)
    result              = models.CharField(max_length=20)
    submitted_at        = models.DateTimeField(auto_now_add=True)

class CyberModel(models.Model):
    algorithm  = models.CharField(max_length=100)
    accuracy   = models.FloatField()
    trained_on = models.DateTimeField(auto_now_add=True)


# Create your models here.
