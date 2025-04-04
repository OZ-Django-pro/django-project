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
    # - PUT: 전체 거래 내여 조회
    # - GET: 특정 거래 내역 조회
    # - PATCH: 거래 내역 수정
    # - DELETE: 거래 내역 삭제
    
class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Transaction_History.objects.all()
    serializer_class = TransactionDetailSerializer

    def perform_update(self, serializer):
        """
        거래 수정 시 계좌 잔액 재계산
        :param serializer: 거래 수정 시 사용되는 serializer
        """
        with transaction.atomic():
            # 수정할 거래 내역을 가져옵니다.
            transaction_instance = self.get_object()
            account = transaction_instance.account
            old_amount = transaction_instance.transaction_amount
            new_amount = serializer.validated_data.get("transaction_amount", old_amount)

            # 거래 유형에 따라 계좌 잔액을 업데이트합니다.
            if transaction_instance.transaction_type == "출금":
                account.balance += old_amount
                account.balance -= new_amount
            else:
                account.balance -= old_amount
                account.balance += new_amount

            # 잔액이 부족한 경우 에러 발생
            if account.balance < 0:
                raise ValidationError({"error": "잔액이 부족합니다."})

            # 계좌 잔액을 업데이트하고 저장합니다.
            account.save()
            # 거래 내역을 업데이트하고 balance_after 필드를 업데이트합니다.
            serializer.save(balance_after=account.balance)

    def perform_destroy(self, instance):
        """
        거래 삭제 시 계좌 잔액 되돌리기
        
        :param instance: 삭제할 거래 내역 인스턴스
        """
        with transaction.atomic():
            # 삭제할 거래 내역의 계좌를 가져옵니다.
            account = instance.account

            # 거래 유형에 따라 계좌 잔액을 되돌립니다.
            if instance.transaction_type == "출금":
                account.balance += instance.transaction_amount
            else:
                account.balance -= instance.transaction_amount

            # 잔액이 부족한 경우 에러 발생
            if account.balance < 0:
                raise ValidationError({"error": "잔액이 부족합니다."})

            # 계좌 잔액을 업데이트하고 저장합니다.
            account.save()
            # 거래 내역을 삭제합니다.
            instance.delete()