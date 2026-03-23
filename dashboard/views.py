from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from visualization.models import PredictionLog
from accounts.models import CustomUser, AccountApproval
from .models import SystemStats

@login_required
def user_dashboard_view(request):
    if not request.user.is_approved: return redirect('approval_pending')
    logs = PredictionLog.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, 'dashboard/user_dashboard.html', {'logs': logs})

@login_required
def officer_dashboard_view(request):
    if request.user.role != 'OFFICER': return redirect('user_dashboard')
    total_users  = CustomUser.objects.count()
    total_preds  = PredictionLog.objects.count()
    pending_count = AccountApproval.objects.filter(status='PENDING').count()
    recent_preds = PredictionLog.objects.order_by('-timestamp')[:10]
    SystemStats.objects.update_or_create(id=1, defaults={
        'total_users': total_users, 'total_predictions': total_preds})
    return render(request, 'dashboard/officer_dashboard.html', {
        'total_users': total_users, 'total_preds': total_preds,
        'pending': pending_count, 'recent_preds': recent_preds})

@login_required
def analyst_dashboard_view(request):
    if request.user.role != 'ANALYST': return redirect('user_dashboard')
    all_logs   = PredictionLog.objects.order_by('-timestamp')
    crime_logs = PredictionLog.objects.filter(module='crime').count()
    cyber_logs = PredictionLog.objects.filter(module='cyber').count()
    return render(request, 'dashboard/analyst_dashboard.html', {
        'all_logs': all_logs, 'crime_count': crime_logs, 'cyber_count': cyber_logs})


