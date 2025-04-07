from rest_framework import serializers

from accounts.models import Transaction_History, Accounts
from .models import Accounts

# 계좌 생성 및 조회 serializer
class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'
        read_only_fields = ['account_id', 'created_at', 'updated_at', 'user_id']

    def create(self, validated_data):
    # user_id가 자동으로 추가되는지 확인
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data['user_id'] = request.user
        return super().create(validated_data)

# 계좌 삭제 serializer
class AccountDetailSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = Accounts
        fields = ['account_id', 'account_number', 'bank_code', 'account_type', 'balance', 'message']
        read_only_fields = ['account_id', 'account_number', 'bank_code', 'account_type', 'balance']

    def get_message(self, obj):
        return f"계좌 {obj.account_number}가 삭제되었습니다."



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_History
        fields = [
            'transaction_id',
            'account_id',
            'transaction_amount',
            'balance_after',
            'transaction_type',
            'transaction_timestamp',
        ]
        read_only_fields = ['balance_after']  # balance_after를 읽기 전용으로 설정
    

class TransactionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction_History
        fields = [
            'transaction_timestamp',
            'transaction_id',
            'transaction_type',
            'transaction_amount',
            'transaction_details',
            'balance_after',
        ]




# # # 지수님
# from .models import Accounts, Transaction_History


# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Accounts
#         fields = '__all__'  # 필요시 일부 필드만 지정 가능


# class AccountDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Accounts
#         fields = '__all__'


# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction_History
#         fields = '__all__'


# class TransactionDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction_History
#         fields = '__all__'
