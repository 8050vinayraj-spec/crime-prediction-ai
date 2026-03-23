from django.urls import path
from . import views
urlpatterns = [
    path('user/',    views.user_dashboard_view,    name='user_dashboard'),
    path('officer/', views.officer_dashboard_view, name='officer_dashboard'),
    path('analyst/', views.analyst_dashboard_view, name='analyst_dashboard'),
]
