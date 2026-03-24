import joblib, os, json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CrimeData, CrimeModel
import folium
from django.http import HttpResponse

from visualization.models import PredictionLog

MODEL_PATH   = os.path.join(os.path.dirname(__file__), 'ml', 'crime_model.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'ml', 'label_encoder.pkl')

@login_required
def crime_home_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    return render(request, 'crime_prediction/crime_home.html')

@login_required
def crime_result_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    if request.method == 'POST':
        year     = int(request.POST['year'])
        month    = int(request.POST['month'])
        location = int(request.POST['location'])
        model    = joblib.load(MODEL_PATH)
        le       = joblib.load(ENCODER_PATH)
        encoded  = model.predict([[year, month, location]])[0]
        result   = le.inverse_transform([encoded])[0]
        CrimeData.objects.create(year=year, month=month,
                                 location=str(location), crime_type=result)
        PredictionLog.objects.create(user=request.user, module='crime',
            input_data={'year': year, 'month': month, 'location': location},
            result=result)
        return render(request, 'crime_prediction/crime_result.html',
            {'result': result, 'year': year, 'month': month, 'location': location})
    return redirect('crime_home')

@login_required
def crime_visualization_view(request):
    from django.db.models import Count
    data   = CrimeData.objects.values('crime_type').annotate(count=Count('id'))
    labels = [d['crime_type'] for d in data]
    counts = [d['count'] for d in data]
    return render(request, 'crime_prediction/crime_visualization.html',
                  {'labels': json.dumps(labels), 'counts': json.dumps(counts)})

LOCATION_COORDS = {
    '1':  (13.0827, 80.2707),   # Chennai
    '2':  (19.0760, 72.8777),   # Mumbai
    '3':  (28.7041, 77.1025),   # Delhi
    '4':  (12.9716, 77.5946),   # Bangalore
    '5':  (17.3850, 78.4867),   # Hyderabad
    '6':  (22.5726, 88.3639),   # Kolkata
    '7':  (23.0225, 72.5714),   # Ahmedabad
    '8':  (18.5204, 73.8567),   # Pune
}

CRIME_COLORS = {
    'Theft':     'red',
    'Assault':   'orange',
    'Cybercrime':'blue',
    'Fraud':     'purple',
    'Vandalism': 'gray'
}

@login_required
def crime_heatmap_view(request):
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    crimes = CrimeData.objects.all()
    for crime in crimes:
        coords = LOCATION_COORDS.get(str(crime.location))
        if coords:
            color = CRIME_COLORS.get(crime.crime_type, 'red')
            folium.Marker(
                location=coords,
                popup=f'{crime.crime_type} — {crime.year}/{crime.month}',
                tooltip=crime.crime_type,
                icon=folium.Icon(color=color, icon='exclamation-sign')
            ).add_to(m)
    map_html = m._repr_html_()
    return render(request, 'crime_prediction/crime_heatmap.html',
                  {'map_html': map_html})
import folium
from django.http import HttpResponse

LOCATION_COORDS = {
    '1':  (13.0827, 80.2707),   # Chennai
    '2':  (19.0760, 72.8777),   # Mumbai
    '3':  (28.7041, 77.1025),   # Delhi
    '4':  (12.9716, 77.5946),   # Bangalore
    '5':  (17.3850, 78.4867),   # Hyderabad
    '6':  (22.5726, 88.3639),   # Kolkata
    '7':  (23.0225, 72.5714),   # Ahmedabad
    '8':  (18.5204, 73.8567),   # Pune
}

CRIME_COLORS = {
    'Theft':     'red',
    'Assault':   'orange',
    'Cybercrime':'blue',
    'Fraud':     'purple',
    'Vandalism': 'gray'
}

@login_required
def crime_heatmap_view(request):
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    crimes = CrimeData.objects.all()
    for crime in crimes:
        coords = LOCATION_COORDS.get(str(crime.location))
        if coords:
            color = CRIME_COLORS.get(crime.crime_type, 'red')
            folium.Marker(
                location=coords,
                popup=f'{crime.crime_type} — {crime.year}/{crime.month}',
                tooltip=crime.crime_type,
                icon=folium.Icon(color=color, icon='exclamation-sign')
            ).add_to(m)
    map_html = m._repr_html_()
    return render(request, 'crime_prediction/crime_heatmap.html',
                  {'map_html': map_html})
