from django.urls import path

from .apis import AccountListCreateView, AccountDetailView, TransactionCreateListView, TransactionDetailView

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),  # 계좌 조회 & 생성
    path('accounts/<uuid:pk>/', AccountDetailView.as_view(), name='account-detail'),  # 계좌 삭제
    path("transaction/", TransactionCreateListView.as_view(), name="transaction-create"),  # ✅ 올바르게 수정
    path('transaction/<uuid:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),  # 거래 조회, 수정, 삭제
]