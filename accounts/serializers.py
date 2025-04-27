from rest_framework import serializers
from .models import Accounts, Transaction_History


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'  # 필요시 일부 필드만 지정 가능


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_History
        fields = '__all__'


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_History
        fields = '__all__'
