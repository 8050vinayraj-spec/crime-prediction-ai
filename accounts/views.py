from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser, AccountApproval, LoginActivity

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email    = request.POST['email']
        password = request.POST['password']
        user = CustomUser.objects.create_user(
            username=username, email=email, password=password, role='USER')
        AccountApproval.objects.create(user=user, status='PENDING')
        return redirect('approval_pending')
    return render(request, 'accounts/signup.html')

def login_view(request):
    error = None
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user:
            LoginActivity.objects.create(user=user,
                ip_address=request.META.get('REMOTE_ADDR'))
            if user.is_approved:
                login(request, user)
                if user.role == 'OFFICER':   return redirect('officer_dashboard')
                elif user.role == 'ANALYST': return redirect('analyst_dashboard')
                else:                        return redirect('user_dashboard')
            else:
                return redirect('approval_pending')
        else:
            error = 'Invalid username or password.'
    return render(request, 'accounts/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

def approval_pending_view(request):
    return render(request, 'accounts/approval_pending.html')

@login_required
def officer_approval_view(request):
    if request.user.role != 'OFFICER':
        return redirect('user_dashboard')
    if request.method == 'POST':
        user_id  = request.POST.get('user_id')
        action   = request.POST.get('action')
        target   = CustomUser.objects.get(id=user_id)
        approval = AccountApproval.objects.get(user=target)
        if action == 'approve':
            target.is_approved   = True
            approval.status      = 'APPROVED'
            approval.approved_by = request.user
        elif action == 'reject':
            approval.status = 'REJECTED'
        target.save(); approval.save()
        return redirect('officer_approve')
    pending  = AccountApproval.objects.filter(status='PENDING').select_related('user')
    approved = AccountApproval.objects.filter(status='APPROVED').select_related('user')
    return render(request, 'accounts/officer_dashboard.html',
                  {'pending': pending, 'approved': approved})
