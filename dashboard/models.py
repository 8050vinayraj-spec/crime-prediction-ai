from django.db import models

class SystemStats(models.Model):
    total_users       = models.IntegerField(default=0)
    total_predictions = models.IntegerField(default=0)
    avg_accuracy      = models.FloatField(default=0.0)
    last_updated      = models.DateTimeField(auto_now=True)
