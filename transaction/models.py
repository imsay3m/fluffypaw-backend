from django.db import models

from account.models import UserAccount

# Create your models here.
TRANSACTION_TYPE = [("Deposit", "Deposit"), ("Pay", "Pay")]


class Transaction(models.Model):
    account = models.ForeignKey(
        UserAccount, related_name="transactions", on_delete=models.CASCADE
    )
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE, max_length=20, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
