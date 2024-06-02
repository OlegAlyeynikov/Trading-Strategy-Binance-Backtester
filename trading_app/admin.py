from django.contrib import admin
from .models import HistoricalData, StrategyParameter

admin.site.register(HistoricalData)
admin.site.register(StrategyParameter)