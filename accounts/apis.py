from rest_framework import generics
from .models import Accounts, Transaction_History
from .serializers import TransactionSerializer, TransactionDetailSerializer


class 