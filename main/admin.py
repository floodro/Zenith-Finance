from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'description', 'amount', 'transaction_type')
    list_filter = ('user', 'transaction_type', 'date')
    search_fields = ('description', 'user__username')