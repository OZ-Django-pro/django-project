from django.urls import path
from .views import (
    AccountListCreateView,
    AccountDetailView,
    TransactionListCreateView,
    TransactionDetailView,
)

urlpatterns = [
    # 계좌
    path('', AccountListCreateView.as_view(), name='account-list-create'),
    path('<uuid:pk>/', AccountDetailView.as_view(), name='account-detail'),

    # 거래 내역
    path('transaction/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transaction/<uuid:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
]
