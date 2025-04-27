from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid

# ✅ 사용자 정의 매니저
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수입니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("슈퍼유저는 is_staff=True 여야 합니다.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("슈퍼유저는 is_superuser=True 여야 합니다.")

        return self.create_user(email, password, **extra_fields)

# ✅ 사용자 모델
class User(AbstractUser):
    username = None

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=50, default="Unknown")
    name = models.CharField(max_length=50, default="Unknown")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    email = models.EmailField(unique=True, max_length=50)
    is_active = models.BooleanField(default=True)

    # ✅ 사용자 매니저 연결
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    def __str__(self):
        return self.email

    @property
    def id(self):
        return self.user_id