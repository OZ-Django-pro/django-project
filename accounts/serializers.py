from rest_framework import serializers
from .models import Accounts

# 계좌 serializer
class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__' # 모든 필드값을 불러옴
        read_only_fields = ['account_id', 'created_at', 'updated_at'] # 생성 후 수정이 불가능한 필드