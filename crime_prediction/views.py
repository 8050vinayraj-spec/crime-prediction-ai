import joblib, os, json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CrimeData, CrimeModel
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