import joblib, os, json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PhishingData, CyberModel
from visualization.models import PredictionLog

MODEL_PATH   = os.path.join(os.path.dirname(__file__), 'ml', 'cyber_model.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'ml', 'cyber_encoder.pkl')

@login_required
def phishing_home_view(request):
    if not request.user.is_approved: return redirect('approval_pending')
    return render(request, 'cybercrime/phishing_home.html')

@login_required
def phishing_result_view(request):
    if not request.user.is_approved: return redirect('approval_pending')
    if request.method == 'POST':
        url_length = int(request.POST['url_length'])
        has_ip     = int(request.POST.get('has_ip', 0))
        keywords   = int(request.POST['suspicious_keywords'])
        has_https  = int(request.POST.get('has_https', 0))
        model      = joblib.load(MODEL_PATH)
        le         = joblib.load(ENCODER_PATH)
        encoded    = model.predict([[url_length, has_ip, keywords, has_https]])[0]
        result     = le.inverse_transform([encoded])[0]
        PhishingData.objects.create(url_length=url_length, has_ip=bool(has_ip),
            suspicious_keywords=keywords, has_https=bool(has_https), result=result)
        PredictionLog.objects.create(user=request.user, module='cyber',
            input_data={'url_length': url_length, 'has_ip': has_ip,
                        'keywords': keywords, 'has_https': has_https},
            result=result)
        return render(request, 'cybercrime/phishing_result.html',
                      {'result': result, 'is_phishing': result == 'phishing'})
    return redirect('phishing_home')

@login_required
def phishing_visualization_view(request):
    from django.db.models import Count
    data   = PhishingData.objects.values('result').annotate(count=Count('id'))
    labels = [d['result'] for d in data]
    counts = [d['count'] for d in data]
    return render(request, 'cybercrime/phishing_visualization.html',
                  {'labels': json.dumps(labels), 'counts': json.dumps(counts)})
