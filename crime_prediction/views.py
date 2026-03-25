import joblib, os, json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime

from .models import CrimeData, CrimeModel
from visualization.models import PredictionLog

import folium

# Paths to ML models
MODEL_PATH   = os.path.join(os.path.dirname(__file__), 'ml', 'crime_model.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'ml', 'label_encoder.pkl')

# Location mappings - All major Indian states and UTs
LOCATIONS = {
    '1': 'Andhra Pradesh',
    '2': 'Arunachal Pradesh',
    '3': 'Assam',
    '4': 'Bihar',
    '5': 'Chhattisgarh',
    '6': 'Goa',
    '7': 'Gujarat',
    '8': 'Haryana',
    '9': 'Himachal Pradesh',
    '10': 'Jharkhand',
    '11': 'Karnataka',
    '12': 'Kerala',
    '13': 'Madhya Pradesh',
    '14': 'Maharashtra',
    '15': 'Manipur',
    '16': 'Meghalaya',
    '17': 'Mizoram',
    '18': 'Nagaland',
    '19': 'Odisha',
    '20': 'Punjab',
    '21': 'Rajasthan',
    '22': 'Sikkim',
    '23': 'Tamil Nadu',
    '24': 'Telangana',
    '25': 'Tripura',
    '26': 'Uttar Pradesh',
    '27': 'Uttarakhand',
    '28': 'West Bengal',
    '29': 'Chandigarh',
    '30': 'Delhi',
    '31': 'Jammu & Kashmir',
    '32': 'Ladakh',
    '33': 'Puducherry',
}

# Month names
MONTHS = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

@login_required
def crime_home_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    context = {
        'locations': LOCATIONS,
        'months': MONTHS,
        'current_year': datetime.now().year,
        'current_month': datetime.now().month,
    }
    return render(request, 'crime_prediction/crime_home.html', context)

@login_required
def crime_result_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    if request.method == 'POST':
        year     = int(request.POST['year'])
        month    = int(request.POST['month'])
        location_code = request.POST['location']
        
        # Validate future date
        current_date = datetime.now()
        if year < current_date.year or (year == current_date.year and month < current_date.month):
            return render(request, 'crime_prediction/crime_home.html', {
                'locations': LOCATIONS,
                'months': MONTHS,
                'current_year': current_date.year,
                'current_month': current_date.month,
                'error': 'Please select a future date for prediction.'
            })
        
        location_name = LOCATIONS.get(location_code, str(location_code))

        # Load ML model and encoder
        model    = joblib.load(MODEL_PATH)
        le       = joblib.load(ENCODER_PATH)

        encoded  = model.predict([[year, month, int(location_code)]])[0]
        result   = le.inverse_transform([encoded])[0]

        # Save prediction to DB
        CrimeData.objects.create(
            year=year, month=month,
            location=location_name, crime_type=result
        )
        PredictionLog.objects.create(
            user=request.user, module='crime',
            input_data={'year': year, 'month': month, 'location': location_name},
            result=result
        )

        return render(request, 'crime_prediction/crime_result.html', {
            'result': result,
            'year': year,
            'month': MONTHS[month],
            'location': location_name
        })
    return redirect('crime_home')

@login_required
def crime_visualization_view(request):
    data   = CrimeData.objects.values('crime_type').annotate(count=Count('id'))
    labels = [d['crime_type'] for d in data]
    counts = [d['count'] for d in data]
    return render(request, 'crime_prediction/crime_visualization.html', {
        'labels': json.dumps(labels),
        'counts': json.dumps(counts)
    })

# Coordinates for locations - All Indian States and UTs capitals/major cities
LOCATION_COORDS = {
    'Andhra Pradesh':    (17.3850, 78.4867),  # Hyderabad
    'Arunachal Pradesh': (28.2180, 94.3997),  # Itanagar
    'Assam':             (26.2006, 92.9373),  # Guwahati
    'Bihar':             (25.5941, 85.1376),  # Patna
    'Chhattisgarh':      (21.2514, 81.6296),  # Raipur
    'Goa':               (15.3025, 73.8330),  # Panaji
    'Gujarat':           (23.0225, 72.5714),  # Ahmedabad
    'Haryana':           (28.4089, 77.0784),  # Faridabad
    'Himachal Pradesh':  (31.1471, 77.1734),  # Shimla
    'Jharkhand':         (23.3645, 85.3340),  # Ranchi
    'Karnataka':         (12.9716, 77.5946),  # Bangalore
    'Kerala':            (9.9312, 76.2673),   # Kochi
    'Madhya Pradesh':    (22.7196, 75.8577),  # Indore
    'Maharashtra':       (19.0760, 72.8777),  # Mumbai
    'Manipur':           (24.8170, 94.9062),  # Imphal
    'Meghalaya':         (25.5788, 91.8933),  # Shillong
    'Mizoram':           (23.8103, 93.9469),  # Aizawl
    'Nagaland':          (25.6753, 94.1093),  # Kohima
    'Odisha':            (20.2961, 85.8245),  # Bhubaneswar
    'Punjab':            (30.7333, 76.7794),  # Chandigarh
    'Rajasthan':         (26.9124, 75.7873),  # Jaipur
    'Sikkim':            (27.5330, 88.5122),  # Gangtok
    'Tamil Nadu':        (13.0827, 80.2707),  # Chennai
    'Telangana':         (17.3850, 78.4867),  # Hyderabad
    'Tripura':           (23.8081, 91.2868),  # Agartala
    'Uttar Pradesh':     (26.8467, 80.9462),  # Lucknow
    'Uttarakhand':       (30.3165, 78.0322),  # Dehradun
    'West Bengal':       (22.5726, 88.3639),  # Kolkata
    'Chandigarh':        (30.7333, 76.7794),  # Chandigarh
    'Delhi':             (28.7041, 77.1025),  # Delhi
    'Jammu & Kashmir':   (34.0837, 74.7973),  # Srinagar
    'Ladakh':            (34.1526, 77.5771),  # Leh
    'Puducherry':        (12.0657, 79.8711),  # Puducherry
}

# Colors for crime types
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
    return render(request, 'crime_prediction/crime_heatmap.html', {
        'map_html': map_html
    })