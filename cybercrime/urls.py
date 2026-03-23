from django.urls import path
from . import views
urlpatterns = [
    path('',           views.phishing_home_view,            name='phishing_home'),
    path('result/',    views.phishing_result_view,          name='phishing_result'),
    path('visualize/', views.phishing_visualization_view,   name='phishing_visualization'),
]
