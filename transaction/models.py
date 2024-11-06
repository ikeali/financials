from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'), 
        ('user', 'User')
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')



class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_number = models.CharField(max_length=20, unique=True,)
    bank_name = models.CharField(max_length=100) 
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  

    def update_balance(self, amount):
        """Update the account balance by the specified amount."""
        self.balance += amount
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Account - Balance: {self.balance}"



class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'), 
        ('withdrawal', 'Withdrawal'), 
        ('transfer', 'Transfer')
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'), 
        ('completed', 'Completed'), 
        ('failed', 'Failed')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')  # Sender
    recipient_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='received_transactions')  # Recipient
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)



