from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Transaction(models.Model):
    """Represents a single financial transaction."""
    
    # Choices for the transaction type
    TRANSACTION_TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    
    # Link to the user who owns this transaction
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    
    # Transaction details
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.description} ({self.get_transaction_type_display()})"

    class Meta:
        ordering = ['-date'] # Show the most recent transactions first