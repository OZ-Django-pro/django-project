
from django.urls import path
from users import apis

app_name = 'users'  # URL 네임스페이스

urlpatterns = [
    path('signup/', apis.RegisterAPIView.as_view(), name='signup'),
    path('login/', apis.LoginView.as_view(), name='login'),
    path('logout/', apis.LogoutView.as_view(), name='logout'),
    path('me/', apis.ProfileAPIView.as_view(), name='profile'),
    path('me/update/', apis.ProfileUpdateAPIView.as_view(), name='profile_update'),
    path('delete/', apis.DestroyView.as_view(), name='user_delete'),
]


# 지수님
from django.urls import path
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
