# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # Django 기본 제공 뷰 사용
from . import views # 직접 작성한 views.py와 연결

urlpatterns = [
    path("signup/", views.signup, name="signup"),

    # LoginView: 로그인 로직을 Django가 알아서 처리해줌. 템플릿 경로만 지정하면 됨
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),

    # LogoutView: 로그아웃 로직도 Django가 처리. POST 요청만 받음
    path("logout/", LogoutView.as_view(), name="logout"),

    path("profile/", views.profile, name="profile"),
]