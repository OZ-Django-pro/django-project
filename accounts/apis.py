from rest_framework import generics, permissions
from .models import Accounts
from .serializers import AccountsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db import transaction
from .models import Accounts, Transaction_History
from .serializers import TransactionSerializer, TransactionDetailSerializer

# 계좌 생성 View
class AccountsCreateView(generics.CreateAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    authentication_classes = [JWTAuthentication]  # JWT 인증 사용
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)  # 현재 사용자를 계좌에 연결


class TransactionCreateView(ListCreateAPIView): #class ListCreateAPIView(mixins.ListModelMixin,
                                                #mixins.CreateModelMixin,
                                                #GenericAPIView):
    """
    거래 생성 API (GET, POST 지원)
    - GET: 거래 내역 목록 조회
    - POST: 새로운 거래 생성
    """
    queryset = Transaction_History.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        """
        거래 생성 시 계좌 잔액을 업데이트
        :param serializer: 거래 생성 시 사용되는 serializer
        """
        with transaction.atomic():
            # 거래 생성 시 사용할 계좌와 거래 정보를 가져옵니다.
            account = serializer.validated_data["account"]
            transaction_type = serializer.validated_data["transaction_type"]
            transaction_amount = serializer.validated_data["transaction_amount"]

            # 출금 거래 시 잔액이 부족한 경우 에러 발생
            if transaction_type == "출금" and account.balance < transaction_amount:
                raise ValidationError({"error": "잔액이 부족합니다."})

            # 거래 유형에 따라 계좌 잔액을 업데이트합니다.
            new_balance = (
                account.balance + transaction_amount if transaction_type == "입금"
                else account.balance - transaction_amount
            )

            # 계좌 잔액을 업데이트하고 저장합니다.
            account.balance = new_balance
            account.save()

            # 거래 내역을 생성하고 balance_after 필드를 업데이트합니다.
            serializer.save(balance_after=new_balance)


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    """
    거래 내역 조회, 수정, 삭제 API (GET, PUT, PATCH, DELETE 지원)
    - PUT: 전체 거래 내여 조회
    - GET: 특정 거래 내역 조회
    - PATCH: 거래 내역 수정
    - DELETE: 거래 내역 삭제
    """
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