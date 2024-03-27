from django.contrib import admin
from .models import Transaction


# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "account",
        "amount",
        "balance_after_transaction",
        "transaction_type",
        "timestamp",
    ]
