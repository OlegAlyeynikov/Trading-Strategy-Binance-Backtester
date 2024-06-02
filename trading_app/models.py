from django.db import models


class HistoricalData(models.Model):
    asset = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    open = models.DecimalField(max_digits=20, decimal_places=10)
    high = models.DecimalField(max_digits=20, decimal_places=10)
    low = models.DecimalField(max_digits=20, decimal_places=10)
    close = models.DecimalField(max_digits=20, decimal_places=10)
    volume = models.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        unique_together = ('asset', 'timestamp')


class StrategyParameter(models.Model):
    parameter_name = models.CharField(max_length=50)
    parameter_value = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
