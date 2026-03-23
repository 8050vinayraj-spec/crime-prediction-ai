from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('crime/', include('crime_prediction.urls')),
    path('cyber/', include('cybercrime.urls')),
    path('visualize/', include('visualization.urls')),
    path('dashboard/', include('dashboard.urls')),
    # Direct shortcuts
    path('login/', account_views.login_view, name='login'),
    path('signup/', account_views.signup_view, name='signup'),
    path('logout/', account_views.logout_view, name='logout'),
    path('pending/', account_views.approval_pending_view, name='approval_pending'),
    path('officer/approve/', account_views.officer_approval_view, name='officer_approve'),
    path('', RedirectView.as_view(url='/login/')),
]