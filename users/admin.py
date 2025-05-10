from django.contrib import admin


# Register your models here.

# from .models import User

# admin.site.register(User)    admin.site.register(User) 2번 등록 

from django.contrib.auth.admin import UserAdmin
from users.models import User  #소셜계정 연동시 SocialAccount 추가


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 필수 표시 항목만 설정
    list_display = ['email', 'username', 'nickname', 'is_active', 'is_staff', 'date_joined']
    list_display_links = ['email', 'username']
    search_fields = ['email', 'nickname', 'phone_number']
    list_filter = ['is_active', 'is_staff']
    ordering = ['-date_joined']
    list_editable = ['is_active']

    # 필드셋 간소화
    fieldsets = (
        ('계정 정보', {'fields': ('email', 'password', 'username')}),
        ('개인 정보', {'fields': ('nickname', 'phone_number')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_admin')}),
        ('소속 그룹', {'fields': ('groups', 'user_permissions')}),
    )

    # 사용자 추가 시 필드셋
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )


    readonly_fields = ['is_admin']

