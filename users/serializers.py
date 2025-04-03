from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
# 사용자가 비밀번호를 변경하는 경우, 비밀번호 hasing처리 필수!
from rest_framework_simplejwt.tokens import RefreshToken


# 회원가입 기능(ModelSerializer)
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"] # id는 생성 후, 읽는 기능만 가능

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user



# Login 기능
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('계정이 비활성화되어 있습니다.')

                # JWT 토큰 생성
                refresh = RefreshToken.for_user(user)

                return {
                    'user': user,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            raise serializers.ValidationError('아이디 또는 비밀번호가 다릅니다.')
        raise serializers.ValidationError('아이디와 비밀번호를 모두 입력해주세요.')

# Logout 기능
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Refresh 토큰")

    def validate_refresh(self, value):
        try:
            token = RefreshToken(value)
            token.blacklist()
            return value
        except Exception:
            raise serializers.ValidationError("유효하지 않은 토큰입니다.")



# Profile(출력,User id, email 등) 조회
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# User 정보 수정할 수 있는 기능
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

    def update(self, instance, validated_data):
        if password := validated_data.get("password"):
            validated_data["password"] = make_password(password)
        return super().update(instance, validated_data)