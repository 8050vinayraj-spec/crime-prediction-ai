from django.urls import path
from . import views

urlpatterns = [
    path('crime-charts/', views.charts_crime_view, name='charts_crime'),
    path('cyber-charts/', views.charts_cyber_view, name='charts_cyber'),
]