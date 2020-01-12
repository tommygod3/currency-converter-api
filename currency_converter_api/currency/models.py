from django.db import models

class Currency(models.Model):
    symbol = models.CharField(max_length=3, primary_key=True)
    #name = models.CharField(max_length=100, primary_key=True)
    gbp_rate = models.FloatField()
    last_updated = models.DateTimeField()
