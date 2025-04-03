from rest_framework import generics, permissions
from .models import Accounts, Transaction_History
from .serializers import AccountsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# 계좌 생성
class AccountsCreateView(generics.CreateAPIView):
    queryset = Accounts.objects.all()  # 모든 계좌 데이터를 가져옴
    serializer_class = AccountsSerializer  # 계좌 데이터를 json으로 변환
    authentication_classes = [JWTAuthentication]  # jwt로 유저 인증 (로그인 확인)
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 유저만 접근 가능

    def perform_create(self, serializer):
        # 계좌 생성 시 현재 로그인한 유저를 계좌에 연결
        serializer.save(user_id=self.request.user)
        # 계좌 생성 시 메시지 출력
        print(f"{Accounts.account_number} 계좌가 생성되었습니다.")

# 계좌 조회
class AccountsListView(generics.ListAPIView):
    serializer_class = AccountsSerializer  # 계좌 데이터를 json으로 변환
    authentication_classes = [JWTAuthentication]  # jwt로 유저 인증 (로그인 확인)
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 유저만 접근 가능

    def get_queryset(self):
        # 현재 로그인한 유저의 계좌만 조회
        return Accounts.objects.filter(user_id=self.request.user)

# 계좌 삭제
class AccountsDeleteView(generics.DestroyAPIView):
    queryset = Accounts.objects.all()  # 모든 계좌 데이터를 가져옴
    serializer_class = AccountsSerializer  # 계좌 데이터를 json으로 변환하는 도구
    authentication_classes = [JWTAuthentication]  # jwt로 유저 인증 (로그인 확인)
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 유저만 접근 가능

    def perform_destroy(self, instance):
        # 계좌 삭제 메시지 출력
        print(f"{instance.account_number} 계좌가 삭제되었습니다.")
        # 실제로 계좌 삭제
        instance.delete()
