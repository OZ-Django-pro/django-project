from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User
from users.serializers import (RegisterSerializer, ProfileSerializer,
                               ProfileUpdateSerializer, LoginSerializer, LogoutSerializer)

#로그아웃 import
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# 회원탈퇴 import
from rest_framework.generics import DestroyAPIView


#회원가입
class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all() # Model
    serializer_class = RegisterSerializer # Serializer

# 로그인
class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        # serializer 유효성 검사는 자동으로 처리됨
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        response = Response(
            {
                "message": "로그인 성공",
                "user": validated_data['user'].username
            },
            status=status.HTTP_200_OK
        )

        # 쿠키 설정
        response.set_cookie(
            'access',
            validated_data['access'],
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=60 * 60 * 24
        )

        response.set_cookie(
            'refresh',
            validated_data['refresh'],
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=60 * 60 * 24 * 7
        )

        return response

# user프로필 표시, 사용자 정보확인, 로그인 상태확인
class ProfileAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated] # 인증된 사용자만 접근
    authentication_classes = [JWTAuthentication] # JWT 인증
    # Retrieve = get_object -> serializer로 반환
    def get_object(self):
        return self.request.user


#회원 프로필 조회, 수정
class ProfileUpdateAPIView(RetrieveAPIView): # Retrieve 기능에 def get,put,patch 기능 포함되어있음
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileSerializer
        elif self.request.method == 'PATCH':
            return ProfileUpdateSerializer # 모델 입력해줘야 함

# Logout 기능
class LogoutView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 쿠키 삭제를 위한 응답 생성
        response = Response(
            {"message": "로그아웃 되었습니다."},
            status=status.HTTP_205_RESET_CONTENT
        )

        # 쿠키에서 토큰 삭제
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response


# 회원탈퇴 기능
class DestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        self.perform_destroy(user)

        # 쿠키에서 토큰 삭제
        response = Response(
            {"message": "Deleted successfully 회원탈퇴가 완료되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response