from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('USER',    'User'),
        ('OFFICER', 'Officer'),
        ('ANALYST', 'Analyst'),
    ]
    role        = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} ({self.role})'

class LoginActivity(models.Model):
    user       = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp  = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} at {self.timestamp}'

class AccountApproval(models.Model):
    STATUS_CHOICES = [
        ('PENDING',  'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    user        = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(CustomUser, null=True, blank=True,
                    on_delete=models.SET_NULL, related_name='approvals_given')
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f'{self.user.username} — {self.status}'

