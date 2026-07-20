# 💚 25기 4주차 팀 과제 PR – 숫자 카드 게임 💚

---

## ✅ 과제 개요

- **과제명:** 피로그래머 숫자 카드 게임
- **기술스택:** Django, HTML/CSS/JS, docker
- **요구사항:** 게임 기능 구현, 도커 이미지 배포 및 컴포즈 구현
- **노션링크:** https://app.notion.com/p/1-8d1ecc3b753182289524811f91cf7405
- **도커이미지배포:** https://hub.docker.com/r/freudes0/piro25-cardgame

---

## 👥 팀원 및 역할 분담

| 이름 | 담당 기능 |
| --- | --- |
| 한지수 | 로그인/회원가입 (소셜+일반) |
| 임현아 | 숫자 카드 생성 및 공격 |
| 정현민 | 반격 기능, 게임 취소 기능 |
| 이환희 | 점수 계산 및 저장, 도커 작성 및 이미지 배포 |
| 정다희 | 게임 리스트 페이지, 게임 상세 페이지, 프론트엔드 완성(전체 CSS 통일) |

## 개인 브랜치명
feat/이름이니셜

✅ **모든 팀원이 직접 커밋 및 구현에 참여하였습니다.**

---

## 🔧 구현 기능 체크리스트

| 기능 | 구현 여부 | 설명 |
| --- | --- | --- |
| 로그인/회원가입 | ✅ | (필수)소셜 로그인, (선택)일반 로그인 |
| 숫자 카드 생성 및 공격 | ✅ | 랜덤 카드 5개 중 1개 선택 + 공격 대상 지정 |
| 반격 기능 구현 | ✅ | 카드 선택 → 즉시 결과 반영 |
| 점수 계산 및 저장 | ✅ | 승/패/무 처리, 점수 증감 |
| 게임 리스트 페이지 | ✅ | 상태별 게임 분기: 진행중 / 반격대기 / 종료 |
| 게임 상세 페이지 | ✅ | 카드, 결과, 버튼 상태 표시 |
| 게임 취소 기능 | ✅ | 반격 전 본인 공격 게임만 삭제 가능 |
| 랭킹 페이지 | ✅ | 유저별 누적 점수 정렬 및 표시 |
| 프론트엔드 완성 | ✅ | HTML/CSS 스타일링, 버튼 UI 등 |
| 도커 이미지 배포 | ✅ | 배포한 도커 허브 링크 등 |
| 도커 컴포즈 구현 | ✅ | |

---

## 🔗 협업 도구 사용 내역

| 도구 | 사용 여부 | 링크 또는 설명 |
| --- | --- | --- |
| 노션 | ✅ | (https://app.notion.com/p/1-8d1ecc3b753182289524811f91cf7405) – **공개 설정 필수** |
| (챌린지)피그마 | ✅ | (https://www.figma.com/design/LXk4l347Y1UNF2W2bqVV5p/piro25_card_game?node-id=0-1&p=f&t=m1RTgWPupr8lRnUN-0) <img width="1760" height="438" alt="image" src="https://github.com/user-attachments/assets/100c377e-1ddf-43ec-88ef-efdf33977baa" />
|
| (챌린지)기타 도구 | / ❌ | [선택 사항] |
| (챌린지)추가 기능 구현 | / ❌ | 구현 설명 |

---

## 🧠 어려웠던 점 / 고민한 부분(선택)

> 
> 

---

## 🙆 기타 사항

> 챌린지 등 추가로 공유할 내용이 있다면 적어주세요.
> 

# 🃏 Piro25_CardGame

피로그래밍 25기 마지막 팀 과제 — 피로그래머 숫자 카드 게임

유저 간 숫자 카드 대결 웹 서비스입니다. 카드를 골라 상대에게 공격을 걸고, 상대가 반격하면 승패가 결정되어 점수가 오르내립니다. 누적 점수로 랭킹이 매겨집니다.

## 🛠 기술 스택

- **Backend**: Django
- **Frontend**: HTML / CSS / JS (Django 템플릿)
- **인증**: 소셜 로그인 (Google / Naver / Kakao)
- **배포**: Docker / Docker Compose

## 📁 프로젝트 구조

```
Piro25_CardGame/
├── config/          # 프로젝트 설정 (settings, urls)
├── accounts/        # 유저 · 인증 (커스텀 User, 소셜 로그인)
├── games/           # 게임 핵심 로직 (공격 / 반격 / 취소 / 결과)
├── ranking/         # 랭킹 리그
├── templates/       # 공통 base.html
├── static/          # 공통 css / js
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── manage.py
```

앱은 역할별로 나뉘어 있습니다. 각자 담당 앱 안에서 작업하면 충돌이 최소화됩니다.

---

## 🚀 시작하기

### 1. 레포 클론 & develop 브랜치로 이동

```bash
git clone https://github.com/Pirogramming-25/Piro25_CardGame_1.git
cd Piro25_CardGame_1
git switch develop
```

> 기본 브랜치가 `main`일 수 있으니 반드시 `develop`으로 이동한 뒤 작업을 시작하세요.

### 2. 가상환경 생성 & 패키지 설치

```bash
python -m venv venv

# 활성화
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. 환경변수(.env) 설정

```bash
cp .env.example .env          # Windows: copy .env.example .env
```

`.env.example`은 키 이름만 있는 껍데기입니다. **실제 값을 채워야 서버가 뜹니다.**

- `SECRET_KEY`, 소셜 로그인 키(Google / Naver / Kakao) 등 민감한 값은 **git에 올라가지 않습니다.**
- 이 값들은 팀 리더가 디스코드 DM / 노션 비공개 페이지 등 안전한 경로로 별도 전달합니다.
- ⚠️ `.env` 파일은 절대 커밋하지 마세요. (`.gitignore`에 이미 포함되어 있습니다.)

### 4. 마이그레이션 적용

```bash
python manage.py migrate
python manage.py createsuperuser   # 선택: admin으로 데이터 확인용
```

### 5. 서버 실행 확인

```bash
python manage.py check
python manage.py runserver
```

`check` 통과 후 `http://127.0.0.1:8000` 이 뜨면 세팅 완료입니다. 🎉

---

## 🌿 Git 협업 규칙

### 브랜치 전략

- `main` : 최종 제출용 (**직접 머지 금지**)
- `develop` : 통합 브랜치 (여기서 각자 개인 브랜치를 땀)
- 개인 브랜치 : **자기 이름으로** 브랜치를 파서 작업

### 작업 흐름

```bash
git switch develop
git pull                          # 최신 develop 상태로 동기화
git switch -c 이름           # 자기 이름으로 브랜치 생성

# ... 작업 & 커밋 ...

git push origin 이름        # push 후 develop 대상으로 PR 생성
```

- 작업은 항상 `develop`에서 딴 **자기 이름 브랜치**에서 진행합니다.
- 완료되면 **`develop` 대상으로 PR**을 올립니다. (`main`에 직접 머지 금지)
- 커밋은 팀원 각자 자기 몫을 직접 남깁니다.

---

## ⚠️ 팀 필수 규칙

- **마이그레이션 파일(`*/migrations/0001_*.py`)은 반드시 커밋합니다.** 무시하면 팀원 간 DB 스키마가 어긋납니다.
- **새 패키지를 설치하면 반드시 `requirements.txt`를 갱신해서 커밋하세요.**
  ```bash
  pip freeze > requirements.txt
  ```
  갱신을 깜빡하면 다른 팀원이 pull 후 "나는 안 돌아간다" 상황이 발생합니다.
- `.env`, 소셜 로그인 키 등 민감 정보는 **절대 커밋하지 않습니다.**
