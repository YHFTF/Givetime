## 🚀 프로젝트 실행 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

> `Django`, `channels`, `daphne`, `Pillow` 등이 설치됩니다.

---

### 2. 데이터베이스 구조 동기화

```bash
python manage.py makemigrations
python manage.py migrate
```

> 모델 변경사항을 반영해 DB 스키마를 생성합니다.

---

### 3. 장고 개발 서버 실행 (정적 파일/일반 요청)

```bash
python manage.py runserver
```

> 기본적으로 8000번 포트에서 실행되며, 정적 파일 및 일반 페이지 요청을 처리합니다.

---

### 4. Daphne ASGI 서버 실행 (웹소켓 전용)

```bash
daphne -p 8001 Givetime.asgi:application
```

> 실시간 채팅 등 **웹소켓 기능**은 `daphne` 서버를 통해 처리됩니다.
> 프론트엔드에서는 `ws://localhost:8001/...` 주소로 연결됩니다.

### 5. 채팅 기능 사용 팁

- 채팅 목록 화면에서 닉네임을 검색해 원하는 사용자와 대화를 시작할 수 있습니다.

---

### 📌 추가 팁

- `.env` 또는 `settings.py`에서 `ALLOWED_HOSTS`, `DEBUG` 등의 설정도 확인해 주세요.
- 웹소켓 연결을 테스트하려면 브라우저 콘솔 또는 개발자 도구의 네트워크 탭을 확인하세요.
- Django admin을 사용하려면 슈퍼유저를 생성하세요:

```bash
python manage.py createsuperuser
```

### 구글 지도 API 키 설정

게시글 작성 화면에서는 구글 맵 API를 사용합니다. 
.env 에 GOOGLE_MAPS_API_KEY=API키
를 넣어주세요.
---

### EXP 포인트 시스템

- **획득 방법**
  - 재능기부 게시글 참여자가 "참여완료" 후 남긴 평점(1~5점)이 게시글 작성자의 EXP로 적립됩니다.
  - 관리자는 필요에 따라 특정 사용자의 EXP를 직접 조정할 수 있습니다.

- **랭크 기준**
  - 하수: 0~99 EXP
  - 중수: 100~499 EXP
  - 고수: 500 EXP 이상

- **혜택**
  - 랭크에 따라 프로필에서 보여지는 등급 배지가 달라집니다.
  - 향후 이벤트 참여권 등 추가 혜택에 활용될 수 있습니다.
