from django.urls import path
from . import views
urlpatterns = [
    path('signup/',          views.signup_view,           name='signup'),
    path('login/',           views.login_view,            name='login'),
    path('logout/',          views.logout_view,           name='logout'),
    path('pending/',         views.approval_pending_view, name='approval_pending'),
    path('officer/approve/', views.officer_approval_view, name='officer_approve'),
]

