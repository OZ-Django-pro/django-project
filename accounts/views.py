from rest_framework import generics
from .models import Accounts, Transaction_History
from .serializers import (
    AccountSerializer,
    AccountDetailSerializer,
    TransactionSerializer,
    TransactionDetailSerializer
)


# 지수님

# 계좌 목록 & 생성
class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer


# 특정 계좌 조회 & 삭제
class AccountDetailView(generics.RetrieveDestroyAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountDetailSerializer


# 거래 내역 전체 조회 & 추가
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction_History.objects.all()
    serializer_class = TransactionSerializer


# 특정 거래 내역 조회 & 수정 & 삭제
class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction_History.objects.all()
    serializer_class = TransactionDetailSerializer
