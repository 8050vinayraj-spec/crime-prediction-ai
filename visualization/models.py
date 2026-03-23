from django.db import models
from django.conf import settings

class PredictionLog(models.Model):
    MODULE_CHOICES = [('crime', 'Crime'), ('cyber', 'Cybercrime')]
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module     = models.CharField(max_length=10, choices=MODULE_CHOICES)
    input_data = models.JSONField()
    result     = models.CharField(max_length=200)
    timestamp  = models.DateTimeField(auto_now_add=True)

