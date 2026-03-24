from django.db import models

class CrimeData(models.Model):
    year        = models.IntegerField()
    month       = models.IntegerField()
    location    = models.CharField(max_length=100)
    crime_type  = models.CharField(max_length=100)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.crime_type} at {self.location} ({self.year}/{self.month})'

class CrimeModel(models.Model):
    algorithm  = models.CharField(max_length=100)
    accuracy   = models.FloatField()
    trained_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.algorithm} — {self.accuracy:.2%}'