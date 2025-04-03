from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User
from users.serializers import UserSignUpSerializer, UserMeReadSerializer, UserMeUpdateSerializer, LoginSerializer

#로그아웃 import
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


#회원가입
class UserSignUpAPIView(CreateAPIView):
    queryset = User.objects.all() # Model
    serializer_class = UserSignUpSerializer # Serializer

# 로그인
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # 시리얼라이저에서 검증된 데이터 가져오기
            validated_data = serializer.validated_data

            # Response 객체 생성
            response = Response(
                {
                    "message": "로그인 성공",
                    "user": validated_data['user'].username
                },
                status=status.HTTP_200_OK
            )
            # 쿠키에 토큰 저장
            response.set_cookie(
                'access',
                validated_data['access'],
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=60 * 60 * 24  # 1일
            )

            response.set_cookie(
                'refresh',
                validated_data['refresh'],
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=60 * 60 * 24 * 7  # 7일
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# user프로필 표시, 사용자 정보확인, 로그인 상태확인
class UserMeAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserMeReadSerializer
    permission_classes = [IsAuthenticated] # 인증된 사용자만 접근
    authentication_classes = [JWTAuthentication] # JWT 인증
    # Retrieve = get_object -> serializer로 반환
    def get_object(self):
        return self.request.user


#회원 프로필 조회, 수정
class UserMeUpdateAPIView(RetrieveAPIView): # Retrieve 기능에 def get,put,patch 기능 포함되어있음
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserMeReadSerializer
        elif self.request.method == 'PATCH':
            return UserMeUpdateSerializer # 모델 입력해줘야 함

# Logout 기능
class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # 인증된 사용자만 이 뷰에 접근가능

    #POST 메서드
    def post(self, request):
        try:
            refresh_token = request.data["refresh"] # 리프레시 토큰 추출
            token = RefreshToken(refresh_token)     # 토큰생성
            token.blacklist()                       # 블랙리스트에 토큰 추가
            return Response(                        # 로그아웃 성공시 응답반환
                {"message": "로그아웃 되었습니다."},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:                      # 에외처리
            return Response(
                {"error": "잘못된 접근입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )