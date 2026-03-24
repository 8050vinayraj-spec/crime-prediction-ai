from django.urls import path
from . import views

urlpatterns = [
    path('', views.crime_home_view, name='crime_home'),
    path('result/', views.crime_result_view, name='crime_result'),
    path('visualize/', views.crime_visualization_view, name='crime_visualization'),
    path('heatmap/', views.crime_heatmap_view, name='crime_heatmap'),
]