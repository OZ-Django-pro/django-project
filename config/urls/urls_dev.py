"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from django.contrib import admin

from users import apis





schema_view = get_schema_view(
    openapi.Info(
        title="Mini Project API",
        default_version='v1',
        description="API 문서",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
# POST /users/ -> 회원가입
    path("", apis.UserSignUpAPIView.as_view(), name="user_sign_up"),
    # POST /users/login -> 로그인
    path('login/', apis.LoginView.as_view(), name='user_login'),
    path('logout/', apis.LogoutView.as_view(), name='user_logout'),
    path('me/', apis.UserMeAPIView.as_view(), name="user_me"),

]