from rest_framework import generics, permissions, status

from .models import Accounts
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db import transaction
from .models import Accounts, Transaction_History
from .serializers import TransactionSerializer, TransactionDetailSerializer, AccountDetailSerializer, AccountsSerializer

import logging
from rest_framework import serializers


# 계좌 생성 및 조회
class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 현재 로그인한 유저가 생성한 계좌만 조회 가능
        return Accounts.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        # 계좌 생성 시, 로그인한 유저를 자동 할당
        serializer.save(user_id=self.request.user)
        print(f"{serializer.instance.account_number} 계좌가 생성되었습니다.")

# 계좌 삭제
class AccountDetailView(generics.DestroyAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        account_number = instance.account_number
        self.perform_destroy(instance)

        return Response(
            {"message": f"계좌 {account_number}가 삭제되었습니다."},
            status=status.HTTP_200_OK
        )

class TransactionCreateListView(generics.ListCreateAPIView):
    
    serializer_class = TransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 현재 로그인한 사용자의 계좌와 관련된 거래 내역만 반환
        user_id = self.request.user.id
        accounts = Accounts.objects.filter(user_id=user_id)
        return Transaction_History.objects.filter(account_id__in=[account.account_id for account in accounts])

    def perform_create(self, serializer):
        with transaction.atomic():
            account_id = serializer.validated_data["account_id"]
            transaction_type = serializer.validated_data["transaction_type"]
            transaction_amount = serializer.validated_data["transaction_amount"]

            # 계좌 정보를 가져옵니다.
            account = account_id

            # 출금 거래 시 잔액이 부족한 경우 에러 발생
            if transaction_type == "WITHDRAW" and account.balance < transaction_amount:
                raise serializers.ValidationError({"error": "잔액이 부족합니다."})

            # 거래 유형에 따라 계좌 잔액을 업데이트합니다.
            new_balance = (
                account.balance + transaction_amount if transaction_type == "DEPOSIT"
                else account.balance - transaction_amount
            )

            # 계좌 잔액을 업데이트하고 저장합니다.
            account.balance = new_balance
            account.save()

            # 거래 내역을 생성하고 balance_after 필드를 업데이트합니다.
            serializer.save(balance_after=new_balance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

#거래 내역 조회
    
    # 거래 내역 조회, 수정, 삭제 API (GET, PUT, PATCH, DELETE 지원)
    # 
    # - GET: 특정 거래 내역 조회
    # - PATCH: 거래 내역 수정
    # - DELETE: 거래 내역 삭제
    
class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Transaction_History.objects.all()
    serializer_class = TransactionDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        거래 수정 시 계좌 잔액 재계산
        PATCH 요청으로 수정된 거래 금액을 반영하여 계좌 잔액 업데이트
        """
        with transaction.atomic():
            transaction_instance = self.get_object()
            account = transaction_instance.account_id

            old_amount = transaction_instance.transaction_amount
            new_amount = serializer.validated_data.get("transaction_amount", old_amount)

            if transaction_instance.transaction_type == "WITHDRAW":
                account.balance += old_amount  # 기존 금액 복구
                account.balance -= new_amount  # 새로운 금액 차감
            else:
                account.balance -= old_amount  # 기존 금액 차감
                account.balance += new_amount  # 새로운 금액 추가

            if account.balance < 0:
                raise ValidationError({"error": "잔액이 부족합니다."})

            account.save()
            serializer.save(balance_after=account.balance)

    def perform_destroy(self, instance):
        """
        거래 삭제 시 거래 내역만 삭제하고 잔액은 유지
        DELETE 요청에서는 계좌 잔액은 변경하지 않음
        """
        with transaction.atomic():
            instance.delete()