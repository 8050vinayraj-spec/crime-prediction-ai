from django.urls import path
from . import views

urlpatterns = [
    path('', views.phishing_home_view, name='phishing_home'),
    path('result/', views.phishing_result_view, name='phishing_result'),
    path('visualize/', views.phishing_visualization_view, name='phishing_visualization'),
    path('ssl-check/', views.ssl_checker_view, name='ssl_checker'),
    path('password-check/', views.password_checker_view, name='password_checker'),
    path('ip-check/', views.ip_checker_view, name='ip_checker'),
    path('file-scan/', views.file_scanner_view, name='file_scanner'),
    path('email-analyse/', views.email_analyser_view, name='email_analyser'),
    path('port-scan/', views.port_scanner_view, name='port_scanner'),
    path('threat-intel/', views.threat_intel_view, name='threat_intel'),
    path('breach-check/', views.breach_checker_view, name='breach_checker'),
    path('whois/', views.whois_lookup_view, name='whois_lookup'),





]
