import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import PredictionLog

@login_required
def charts_crime_view(request):
    logs   = PredictionLog.objects.filter(module='crime')
    data   = logs.values('result').annotate(count=Count('id'))
    labels = [d['result'] for d in data]
    counts = [d['count'] for d in data]
    recent = logs.order_by('-timestamp')[:10]
    return render(request, 'visualization/charts_crime.html',
                  {'labels': json.dumps(labels), 'counts': json.dumps(counts), 'recent': recent})

@login_required
def charts_cyber_view(request):
    logs   = PredictionLog.objects.filter(module='cyber')
    data   = logs.values('result').annotate(count=Count('id'))
    labels = [d['result'] for d in data]
    counts = [d['count'] for d in data]
    recent = logs.order_by('-timestamp')[:10]
    return render(request, 'visualization/charts_cyber.html',
                  {'labels': json.dumps(labels), 'counts': json.dumps(counts), 'recent': recent})

