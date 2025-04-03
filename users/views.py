from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

# 회원가입
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# 로그인
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

# 로그아웃 (JWT 토큰 블랙리스트 처리)
class LogoutView(TokenBlacklistView):
    permission_classes = [AllowAny]
