import joblib, os, json
from urllib.parse import urlparse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PhishingData, CyberModel
from visualization.models import PredictionLog

MODEL_PATH   = os.path.join(os.path.dirname(__file__), 'ml', 'cyber_model.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'ml', 'cyber_encoder.pkl')

def extract_features(url):
    parsed        = urlparse(url)
    using_ip      = 1  if any(c.isdigit() for c in parsed.netloc.split('.')) and \
                    all(c.isdigit() or c == '.' for c in parsed.netloc) else -1
    long_url      = 1  if len(url) > 75   else -1
    short_url     = 1  if len(url) < 20   else -1
    https         = 1  if parsed.scheme == 'https' else -1
    sub_domains   = 1  if parsed.netloc.count('.') > 2 else -1
    prefix_suffix = 1  if '-' in parsed.netloc else -1
    web_traffic   = -1
    page_rank     = -1
    google_index  = 1
    links_point   = -1
    return [using_ip, long_url, short_url, https, sub_domains,
            prefix_suffix, web_traffic, page_rank, google_index, links_point]

@login_required
def phishing_home_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    return render(request, 'cybercrime/phishing_home.html')

@login_required
def phishing_result_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    if request.method == 'POST':
        url      = request.POST['url']
        features = extract_features(url)
        model    = joblib.load(MODEL_PATH)
        le       = joblib.load(ENCODER_PATH)
        encoded  = model.predict([features])[0]
        result   = le.inverse_transform([encoded])[0]
        PhishingData.objects.create(
            url_length=len(url),
            has_ip=features[0] == 1,
            suspicious_keywords=0,
            has_https=features[3] == 1,
            result=result)
        PredictionLog.objects.create(
            user=request.user,
            module='cyber',
            input_data={'url': url},
            result=result)
        return render(request, 'cybercrime/phishing_result.html',
                      {'result': result,
                       'is_phishing': result == 'phishing',
                       'url': url})
    return redirect('phishing_home')

@login_required
def phishing_visualization_view(request):
    from django.db.models import Count
    data   = PhishingData.objects.values('result').annotate(count=Count('id'))
    labels = [d['result'] for d in data]
    counts = [d['count'] for d in data]
    return render(request, 'cybercrime/phishing_visualization.html',
                  {'labels': json.dumps(labels), 'counts': json.dumps(counts)})