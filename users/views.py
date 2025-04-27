from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, ProfileSerializer

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

class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user