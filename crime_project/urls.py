from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('crime/', include('crime_prediction.urls')),
    path('cyber/', include('cybercrime.urls')),
    path('visualize/', include('visualization.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('accounts.urls')),
]