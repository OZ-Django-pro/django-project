from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    # 커스텀 필드
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=50, default="Unknown")
    name = models.CharField(max_length=50, default="Unknown")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_admin = models.BooleanField(default=False)  # 관리자 여부 (기본값: False)

    # 옵션이 추가된 기본 필드
    email = models.EmailField(unique=True, max_length=50) # 이메일 중복 가입 방지 (unique=True 사용)
    is_active = models.BooleanField(default=True) # 계정 활성화 여부 (기본값: True)

    # USERNAME_FIELD: 로그인 시 사용할 필드 (기본값은 'username', 여기서는 'email'로 변경)
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS: 사용자 생성 시 필수로 입력해야 하는 필드
    REQUIRED_FIELDS = ['name', 'phone_number']

    def __str__(self):
        return self.email  # 객체를 문자열로 표현할 때 이메일 반환
