import joblib, os, json
from urllib.parse import urlparse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PhishingData, CyberModel
from visualization.models import PredictionLog
import ssl, socket
from datetime import datetime
import hashlib, re
from django.conf import settings as django_settings
import email
from email import policy
from email.parser import HeaderParser
import folium
from django.http import HttpResponse
import whois
import requests
from crime_prediction.models import CrimeData, CrimeModel

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

@login_required
def ssl_checker_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    result = None
    error  = None
    if request.method == 'POST':
        domain = request.POST['domain'].replace('https://','').replace('http://','').strip('/').split('/')[0]
        try:
            ctx  = ssl.create_default_context()
            conn = ctx.wrap_socket(
                socket.socket(socket.AF_INET),
                server_hostname=domain)
            conn.settimeout(5)
            conn.connect((domain, 443))
            cert = conn.getpeercert()
            conn.close()
            expire_str = cert['notAfter']
            expire_date = datetime.strptime(expire_str, '%b %d %H:%M:%S %Y %Z')
            days_left = (expire_date - datetime.utcnow()).days
            result = {
                'domain':     domain,
                'issued_to':  cert.get('subject', [[('', '')]])[0][0][1],
                'issued_by':  cert.get('issuer', [[('', '')]])[1][0][1],
                'expires':    expire_date.strftime('%d %B %Y'),
                'days_left':  days_left,
                'valid':      days_left > 0,
                'status':     'Valid' if days_left > 0 else 'Expired'
            }
        except Exception as e:
            error = f'Could not retrieve SSL certificate: {str(e)}'
    return render(request, 'cybercrime/ssl_checker.html',
                  {'result': result, 'error': error})

@login_required
def password_checker_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    result = None
    if request.method == 'POST':
        password = request.POST['password']
        score    = 0
        feedback = []
        if len(password) >= 8:  score += 1
        else: feedback.append('Use at least 8 characters')
        if re.search(r'[A-Z]', password): score += 1
        else: feedback.append('Add uppercase letters')
        if re.search(r'[a-z]', password): score += 1
        else: feedback.append('Add lowercase letters')
        if re.search(r'[0-9]', password): score += 1
        else: feedback.append('Add numbers')
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 1
        else: feedback.append('Add special characters (!@#$)')
        strength = ['Very Weak','Weak','Fair','Strong','Very Strong'][score-1] if score > 0 else 'Very Weak'
        color    = ['danger','danger','warning','info','success'][score-1] if score > 0 else 'danger'
        # Check HaveIBeenPwned API
        breached = False
        breach_count = 0
        try:
            sha1     = hashlib.sha1(password.encode()).hexdigest().upper()
            prefix   = sha1[:5]
            suffix   = sha1[5:]
            response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}',
                                    timeout=5)
            hashes   = response.text.splitlines()
            for h in hashes:
                parts = h.split(':')
                if parts[0] == suffix:
                    breached     = True
                    breach_count = int(parts[1])
                    break
        except: pass
        result = {
            'score':       score,
            'strength':    strength,
            'color':       color,
            'feedback':    feedback,
            'breached':    breached,
            'breach_count':breach_count,
            'percent':     score * 20
        }
    return render(request, 'cybercrime/password_checker.html', {'result': result})

@login_required
def ip_checker_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    result = None
    error  = None
    if request.method == 'POST':
        ip = request.POST['ip'].strip()
        try:
            response = requests.get(
                f'http://ip-api.com/json/{ip}?fields=status,message,country,'
                'regionName,city,zip,lat,lon,isp,org,as,proxy,hosting,query',
                timeout=5)
            data = response.json()
            if data.get('status') == 'success':
                result = data
                result['risk'] = 'High' if data.get('proxy') or data.get('hosting') else 'Low'
                result['risk_color'] = 'danger' if result['risk'] == 'High' else 'success'
            else:
                error = data.get('message', 'Invalid IP address')
        except Exception as e:
            error = f'Error: {str(e)}'
    return render(request, 'cybercrime/ip_checker.html',
                  {'result': result, 'error': error})
@login_required
def file_scanner_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    result = None
    error  = None
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded = request.FILES['file']
        content  = uploaded.read()
        md5      = hashlib.md5(content).hexdigest()
        sha256   = hashlib.sha256(content).hexdigest()
        vt_result = None
        try:
            api_key  = django_settings.VIRUSTOTAL_API_KEY
            headers  = {'x-apikey': api_key}
            response = requests.get(
                f'https://www.virustotal.com/api/v3/files/{sha256}',
                headers=headers, timeout=10)
            if response.status_code == 200:
                data     = response.json()
                stats    = data['data']['attributes']['last_analysis_stats']
                vt_result = {
                    'malicious':  stats.get('malicious', 0),
                    'suspicious': stats.get('suspicious', 0),
                    'harmless':   stats.get('harmless', 0),
                    'undetected': stats.get('undetected', 0),
                }
        except: pass
        result = {
            'filename': uploaded.name,
            'size':     len(content),
            'md5':      md5,
            'sha256':   sha256,
            'vt':       vt_result
        }
    return render(request, 'cybercrime/file_scanner.html',
                  {'result': result, 'error': error})
@login_required
def email_analyser_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    result = None
    if request.method == 'POST':
        raw_headers = request.POST['headers']
        parser      = HeaderParser()
        msg         = parser.parsestr(raw_headers)
        suspicious_keywords = ['urgent','verify','click here','limited time',
                               'account suspended','winner','free money','password']
        subject    = msg.get('Subject', '')
        found_kw   = [kw for kw in suspicious_keywords if kw.lower() in subject.lower()]
        result = {
            'from':       msg.get('From', 'N/A'),
            'to':         msg.get('To', 'N/A'),
            'subject':    subject,
            'date':       msg.get('Date', 'N/A'),
            'message_id': msg.get('Message-ID', 'N/A'),
            'received':   msg.get_all('Received', []),
            'spf':        'Pass' if 'spf=pass' in raw_headers.lower() else 'Fail/Missing',
            'dkim':       'Pass' if 'dkim=pass' in raw_headers.lower() else 'Fail/Missing',
            'keywords':   found_kw,
            'suspicious': len(found_kw) > 0 or 'spf=fail' in raw_headers.lower()
        }
    return render(request, 'cybercrime/email_analyser.html', {'result': result})

@login_required
def port_scanner_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    result = None
    error  = None
    if request.method == 'POST':
        target = request.POST['target'].strip()
        ports  = [21, 22, 23, 25, 53, 80, 443, 3306, 3389, 8080, 8443]
        port_names = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 443: 'HTTPS', 3306: 'MySQL',
            3389: 'RDP', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt'
        }
        scan_results = []
        try:
            for port in ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                status = sock.connect_ex((target, port))
                scan_results.append({
                    'port':   port,
                    'name':   port_names.get(port, 'Unknown'),
                    'status': 'Open' if status == 0 else 'Closed',
                    'color':  'danger' if status == 0 else 'success'
                })
                sock.close()
            result = {'target': target, 'ports': scan_results,
                      'open_count': sum(1 for p in scan_results if p['status']=='Open')}
        except Exception as e:
            error = f'Scan failed: {str(e)}'
    return render(request, 'cybercrime/port_scanner.html',
                  {'result': result, 'error': error})


@login_required
def threat_intel_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    articles = []
    error    = None
    try:
        api_key  = django_settings.NEWS_API_KEY
        response = requests.get(
            'https://newsapi.org/v2/everything',
            params={
                'q':        'cybersecurity OR phishing OR malware OR ransomware',
                'sortBy':   'publishedAt',
                'pageSize': 12,
                'language': 'en',
                'apiKey':   api_key
            }, timeout=10)
        data = response.json()
        if data.get('status') == 'ok':
            articles = data.get('articles', [])
        else:
            error = 'Could not fetch threat intelligence feed.'
    except Exception as e:
        error = f'Error: {str(e)}'
    return render(request, 'cybercrime/threat_intel.html',
                  {'articles': articles, 'error': error})

@login_required
def breach_checker_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    result = None
    error  = None
    if request.method == 'POST':
        email = request.POST['email'].strip()
        try:
            headers  = {'hibp-api-key': 'your_hibp_api_key',
                        'user-agent':   'CrimeAI-Project'}
            response = requests.get(
                f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
                headers=headers, timeout=10)
            if response.status_code == 200:
                breaches = response.json()
                result   = {'email': email, 'breaches': breaches,
                            'count': len(breaches), 'found': True}
            elif response.status_code == 404:
                result = {'email': email, 'breaches': [],
                          'count': 0, 'found': False}
            else:
                error = 'API error. Check your HIBP API key.'
        except Exception as e:
            error = f'Error: {str(e)}'
    return render(request, 'cybercrime/breach_checker.html',
                  {'result': result, 'error': error})

@login_required
def whois_lookup_view(request):
    if not request.user.is_approved:
        return redirect('approval_pending')
    result = None
    error  = None
    if request.method == 'POST':
        domain = request.POST['domain'].strip()
        try:
            w = whois.whois(domain)
            result = {
                'domain':     domain,
                'registrar':  w.registrar,
                'created':    str(w.creation_date)[:10] if w.creation_date else 'N/A',
                'expires':    str(w.expiration_date)[:10] if w.expiration_date else 'N/A',
                'updated':    str(w.updated_date)[:10] if w.updated_date else 'N/A',
                'name_servers': w.name_servers,
                'emails':     w.emails,
                'country':    w.country,
            }
        except Exception as e:
            error = f'WHOIS lookup failed: {str(e)}'
    return render(request, 'cybercrime/whois_lookup.html',
                  {'result': result, 'error': error})
