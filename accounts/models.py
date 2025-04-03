from django.db import models
import uuid
from constants import BANK_CODES, ACCOUNT_TYPE, TRANSACTION_TYPE, TRANSACTION_METHOD

from users.models import User



class Accounts(models.Model):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    bank_code = models.CharField(max_length=20, choices=BANK_CODES)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '계좌'
        verbose_name_plural = '계좌목록'

    def __str__(self):
        return f'{self.account_type}-{self.account_number}-{self.bank_code}'

class Transaction_History(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(max_digits=20, decimal_places=2)
    balance_after = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    transaction_method = models.CharField(max_length=20, choices=TRANSACTION_METHOD)
    transaction_details = models.CharField(max_length=100)
    transaction_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-transaction_timestamp']
        verbose_name = '거래 내역'
        verbose_name_plural = '거래 내역 목록'

    def __str__(self):
        return f'{self.transaction_type}-{self.transaction_details}-{self.transaction_timestamp}'