from django.contrib import admin
from .models import Transaction, Profile

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'description', 'amount', 'transaction_type')
    list_filter = ('user', 'transaction_type', 'date')
    search_fields = ('description', 'user__username')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_number')