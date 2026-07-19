# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm  # Django 기본 회원가입 폼
from django.contrib.auth import login                   # 로그인 처리 함수
from django.contrib.auth.decorators import login_required  # 접근 제한 데코레이터

def signup(request):
    if request.method == "POST":           # 폼 제출했을 때
        form = UserCreationForm(request.POST)
        if form.is_valid():                # 입력값이 유효하면
            user = form.save()             # DB에 사용자 저장
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")           # 가입 즉시 로그인 처리 (세션 생성)
            return redirect("profile")     # urls.py의 profile 주소로 이동
    else:                                  # 처음 페이지에 접근했을 때 (GET)
        form = UserCreationForm()          # 빈 폼 생성
    return render(request, "accounts/signup.html", {"form": form})

@login_required  # 로그인 안 한 사용자는 LOGIN_URL로 자동 리다이렉트
def profile(request):
    return render(request, "accounts/profile.html")