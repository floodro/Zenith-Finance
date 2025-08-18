from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    """Extends the default User model to include extra fields."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


# Automatically create a profile for every new user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Category(models.Model):
    """Transaction categories (can be global or user-defined)."""
    KIND_CHOICES = [
        ('EXPENSE', 'Expense'),
        ('INCOME', 'Income'),
        ('TRANSFER', 'Transfer'),
    ]
    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=8, choices=KIND_CHOICES)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('user', 'name', 'parent')
        ordering = ['kind', 'parent__name', 'name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.parent.name} › {self.name}" if self.parent else self.name


class Transaction(models.Model):
    """Represents a single financial transaction."""
    TRANSACTION_TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('TRANSFER', 'Transfer'),
        ('REFUND', 'Refund'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('DEBIT_CARD', 'Debit Card'),
        ('CREDIT_CARD', 'Credit Card'),
        ('E_WALLET', 'E-Wallet'),
        ('CHECK', 'Check'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateField(default=timezone.now)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='transactions')
    merchant = models.CharField(max_length=120, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        type_disp = self.get_transaction_type_display()
        return f"{self.user.username} - {self.description} ({type_disp})"

    class Meta:
        ordering = ['-date', '-id']
