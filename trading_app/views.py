from django.shortcuts import render
from .models import HistoricalData


def index(request):
    data = HistoricalData.objects.all()
    return render(request, 'index.html', {'data': data})
