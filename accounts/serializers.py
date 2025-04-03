from rest_framework import serializers

from accounts.models import Transaction_History, Accounts
from .models import Accounts

# 계좌 serializer
class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__' # 모든 필드값을 불러옴
        read_only_fields = ['account_id', 'created_at', 'updated_at'] # 생성 후 수정이 불가능한 필드



class TransactionSerializer(serializers.ModelSerializer):
    deposit_amount  = serializers.SerializerMethodField()
    withdrawal_amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction_History
        fields = [
            'transaction_timestamp',
            'transaction_type',
            'deposit_amount',
            'withdrawal_amount',
            'balance_after',
        ]

# 입금 거래일 경우 입금 금액 반환
    def get_deposit_amount(self, obj):
        return obj.transaction_amount if obj.transaction_type =="입금" else None
    
# 출금 거래 일경우 출금 금액 반환
    def get_withdrawal_amount(self, obj):
        return obj.transaction_amount if obj.transaction_type =="출금" else None
    

class TransactionDetailSerializer(serializers.ModelSerializer):
    account_info = serializers.SerializerMethodField()

    class Meta:
        model = Transaction_History
        fields = [
            'transaction_timestamp',
            'transaction_id',
            'account_info',
            'transaction_type',
            'transaction_amount',
            'transaction_details',
            'balance_after',
        ]

    #  거래된 계좌 정보를 포함할지 여부를 결정(불필요한 데이터를 줄이고 응답 속도 개선)
    def get_account_info(self, obj):
        if self.context.get('include_account_info'):
            return {
                "account_id":obj.account_id.account_id,
                "account_number": obj.account_id.account_number,
                "bank_code": obj.account_id.bank_code
            }
        return None
    
    # 입금 거래일 경우 입금 금액 반환
    def get_deposit_amount(self, obj):
        return obj.transaction_amount if obj.transaction_type =="입금" else None
    
    # 출금 거래 일경우 출금 금액 반환
    def get_withdrawal_amount(self, obj):
        return obj.transaction_amount if obj.transaction_type =="출금" else None

