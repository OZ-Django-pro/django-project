from rest_framework import generics, permissions
from .models import Accounts
from .serializers import AccountsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# 계좌 생성 View
class AccountsCreateView(generics.CreateAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    authentication_classes = [JWTAuthentication]  # JWT 인증 사용
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)  # 현재 사용자를 계좌에 연결
